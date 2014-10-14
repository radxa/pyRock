/* GPIO library extension for rockchip soc.
 *
 * Copyright (c) 2014 Radxa Limited.
 * http://radxa.com
 *
 * Taken from rockchip pintctrl driver by
 * Copyright (c) 2013 MundoReader S.L.
 * Author: Heiko Stuebner <heiko@sntech.de>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 */


#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/select.h>
#include <pthread.h>
#include <unistd.h>
#include <sched.h>
#include <stdio.h>

#include "gpio_lib.h"
#include "errno.h"

static struct rockchip_pin_bank rk3188_pin_banks[] = {
	PIN_BANK_IOMUX_FLAGS(0, 0x2000a000, 32, "gpio0", IOMUX_GPIO_ONLY, IOMUX_GPIO_ONLY, 0, 0),
	PIN_BANK(1, 0x2003c000, 32, "gpio1"),
	PIN_BANK(2, 0x2003e000, 32, "gpio2"),
	PIN_BANK(3, 0x20080000, 32, "gpio3"),
};

static struct rockchip_pin_ctrl rk3188_pin_ctrl = {
	.pin_banks		= rk3188_pin_banks,
	.nr_banks		= sizeof(rk3188_pin_banks)/sizeof(struct rockchip_pin_bank),
	.label			= "RK3188-GPIO",
	.grf_mux_offset	= 0x60,
	.pmu_base		= (void *)0x20004000,
	.grf_base		= (void *)0x20008000,
};

struct rockchip_pin_ctrl *rkxx_pin_ctrl = &rk3188_pin_ctrl;

/*
 * given a pin number that is local to a pin controller, find out the pin bank
 * and the register base of the pin bank.
 */
static struct rockchip_pin_bank *pin_to_bank(unsigned pin)
{
	struct rockchip_pin_bank *b = rkxx_pin_ctrl->pin_banks;

	while (pin >= (b->pin_base + b->nr_pins))
		b++;

	return b;
}

/* map reg to access */
static int map_reg(void *reg, void **reg_mapped)
{
	int fd;
    unsigned int addr_start, addr_offset;
    unsigned int pagesize, pagemask;
    void *pc;

    fd = open("/dev/mem", O_RDWR);
    if (fd < 0) {
		return -E_MEM_OPEN;
    }

    pagesize = sysconf(_SC_PAGESIZE);
    pagemask = (~(pagesize - 1));

	addr_start = (unsigned int)reg & pagemask;
	addr_offset = (unsigned int)reg & ~pagemask;

	pc = (void *) mmap(0, pagesize * 2, PROT_READ | PROT_WRITE, MAP_SHARED, fd, addr_start);

	if (pc == MAP_FAILED) {
		return -E_MEM_MAP;
	}
    close(fd);

	*reg_mapped = (pc + addr_offset);

	return 0;
}

int rockchip_gpio_init(void) {
	int grf_offs, pmu_offs, i, j;
	int ret;

	struct rockchip_pin_ctrl *ctrl = rkxx_pin_ctrl;
	struct rockchip_pin_bank *bank = ctrl->pin_banks;

	grf_offs = ctrl->grf_mux_offset;
	pmu_offs = ctrl->pmu_mux_offset;

	for (i = 0; i < ctrl->nr_banks; ++i, ++bank ) {
		int bank_pins = 0;

		bank->pin_base = ctrl->nr_pins;
		ctrl->nr_pins += bank->nr_pins;

		/* calculate iomux offsets */
		for (j = 0; j < 4; j++) {
			struct rockchip_iomux *iom = &bank->iomux[j];
			int inc;

			if (bank_pins >= bank->nr_pins)
				break;

			/* preset offset value, set new start value */
			if (iom->offset >= 0) {
				if (iom->type & IOMUX_SOURCE_PMU)
					pmu_offs = iom->offset;
				else
					grf_offs = iom->offset;
			} else { /* set current offset */
				iom->offset = (iom->type & IOMUX_SOURCE_PMU) ?
							pmu_offs : grf_offs;
			}

			/*
			 * Increase offset according to iomux width.
			 * 4bit iomux'es are spread over two registers.
			 */
			inc = (iom->type & IOMUX_WIDTH_4BIT) ? 8 : 4;
			if (iom->type & IOMUX_SOURCE_PMU)
				pmu_offs += inc;
			else
				grf_offs += inc;

			bank_pins += 8;
		}

		ret = map_reg(bank->reg_base, &bank->reg_mapped_base);
		if (ret < 0)
			return ret;
	}

	ret = map_reg(ctrl->pmu_base, &ctrl->pmu_mapped_base);
	if (ret < 0)
		return ret;
	ret = map_reg(ctrl->grf_base, &ctrl->grf_mapped_base);
	if (ret < 0)
		return ret;

    return 0;
}

int rockchip_gpio_set_direction(unsigned int pin, unsigned int input)
{
	struct rockchip_pin_bank *bank = pin_to_bank(pin);
	int ret, offset;
	unsigned int data;

	ret = rockchip_gpio_set_mux(pin, RK_FUNC_GPIO);
	if (ret < 0)
		return ret;

	data = readl(bank->reg_mapped_base + GPIO_SWPORT_DDR);

	/* set bit to 1 for output, 0 for input */
	offset = pin - bank->pin_base;
	if (!input)
		data |= BIT(offset);
	else
		data &= ~BIT(offset);

	writel(data, bank->reg_mapped_base + GPIO_SWPORT_DDR);

	return 0;
}

int rockchip_gpio_set_mux(unsigned int pin, unsigned int mux) {

	struct rockchip_pin_ctrl *info = rkxx_pin_ctrl;
	struct rockchip_pin_bank *bank = pin_to_bank(pin);
	int iomux_num = (pin / 8);
	unsigned int data, offset, mask;
	unsigned char bit;
	void *reg_mapped_base;

	if (iomux_num > 3)
		return -E_MUX_INVAL;

	if (bank->iomux[iomux_num].type & IOMUX_UNROUTED) {
		return -E_MUX_UNROUTED;
	}

	if (bank->iomux[iomux_num].type & IOMUX_GPIO_ONLY) {
		if (mux != RK_FUNC_GPIO) {
			return -E_MUX_GPIOONLY;
		} else {
			return 0;
		}
	}

	reg_mapped_base = (bank->iomux[iomux_num].type & IOMUX_SOURCE_PMU)
				? info->pmu_mapped_base : info->grf_mapped_base;

	/* get basic quadrupel of mux registers and the correct reg inside */
	mask = (bank->iomux[iomux_num].type & IOMUX_WIDTH_4BIT) ? 0xf : 0x3;
	offset = bank->iomux[iomux_num].offset;
	if (bank->iomux[iomux_num].type & IOMUX_WIDTH_4BIT) {
		if ((pin % 8) >= 4)
			offset += 0x4;
		bit = (pin % 4) * 4;
	} else {
		bit = (pin % 8) * 2;
	}

	data = (mask << (bit + 16));
	data |= (mux & mask) << bit;
	writel(data, reg_mapped_base + offset);

    return 0;
}

int rockchip_gpio_get_mux(unsigned int pin) {

	struct rockchip_pin_ctrl *info = rkxx_pin_ctrl;
	struct rockchip_pin_bank *bank = pin_to_bank(pin);
	int iomux_num = (pin / 8);
	unsigned int val, offset, mask;
	unsigned char bit;
	void *reg_mapped_base;

	if (iomux_num > 3)
		return -E_MUX_INVAL;

	if (bank->iomux[iomux_num].type & IOMUX_UNROUTED) {
		return -E_MUX_UNROUTED;
	}

	if (bank->iomux[iomux_num].type & IOMUX_GPIO_ONLY)
		return RK_FUNC_GPIO;

	reg_mapped_base = (bank->iomux[iomux_num].type & IOMUX_SOURCE_PMU)
				? info->pmu_mapped_base : info->grf_mapped_base;

	/* get basic quadrupel of mux registers and the correct reg inside */
	mask = (bank->iomux[iomux_num].type & IOMUX_WIDTH_4BIT) ? 0xf : 0x3;
	offset = bank->iomux[iomux_num].offset;
	if (bank->iomux[iomux_num].type & IOMUX_WIDTH_4BIT) {
		if ((pin % 8) >= 4)
			offset += 0x4;
		bit = (pin % 4) * 4;
	} else {
		bit = (pin % 8) * 2;
	}

	val = readl(reg_mapped_base + offset);

	return ((val >> bit) & mask);
}

int rockchip_gpio_input(unsigned int pin) {

    unsigned int data;
	struct rockchip_pin_bank *bank = pin_to_bank(pin);
	int offset = pin - bank->pin_base;

	rockchip_gpio_set_direction(pin, ROCKCHIP_GPIO_INPUT);

	data = readl(bank->reg_mapped_base + GPIO_EXT_PORT);
	data >>= offset;

    return (data & 0x1);
}

int rockchip_gpio_output(unsigned int pin, unsigned int val) {

	unsigned int data;
	struct rockchip_pin_bank *bank = pin_to_bank(pin);
	void *reg = bank->reg_mapped_base + GPIO_SWPORT_DR;
	int offset = pin - bank->pin_base;

	rockchip_gpio_set_direction(pin, ROCKCHIP_GPIO_OUTPUT);

	data = readl(reg);
	data &= ~BIT(offset);
	if (val)
		data |= BIT(offset);

	writel(data, reg);

    return 0;
}

int rockchip_gpio_pullup(unsigned int pin, unsigned int pull) {

    return 0;
}

