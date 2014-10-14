/* GPIO definition for rockchip soc.
 * Taken from rockchip pinctrl driver by Heiko Stuebner <heiko@sntech.de>
 *
 * Copyright (c) 2014 Radxa Limited.
 * http://radxa.com
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 */

#ifndef _GPIO_LIB_H_
#define _GPIO_LIB_H_

#define RK_GPIO0	0
#define RK_GPIO1	1
#define RK_GPIO2	2
#define RK_GPIO3	3
#define RK_GPIO4	4
#define RK_GPIO6	6

#define RK_FUNC_GPIO	0
#define RK_FUNC_1		1
#define RK_FUNC_2		2

#define ROCKCHIP_GPIO_INPUT		1
#define ROCKCHIP_GPIO_OUTPUT	0

#define ROCKCHIP_PULL_UP		0
#define ROCKCHIP_PULL_DOWN		1

/* GPIO control registers */
#define GPIO_SWPORT_DR		0x00
#define GPIO_SWPORT_DDR		0x04
#define GPIO_INTEN			0x30
#define GPIO_INTMASK		0x34
#define GPIO_INTTYPE_LEVEL	0x38
#define GPIO_INT_POLARITY	0x3c
#define GPIO_INT_STATUS		0x40
#define GPIO_INT_RAWSTATUS	0x44
#define GPIO_DEBOUNCE		0x48
#define GPIO_PORTS_EOI		0x4c
#define GPIO_EXT_PORT		0x50
#define GPIO_LS_SYNC		0x60

#define BIT(nr) (1UL << (nr))

/**
 * Encode variants of iomux registers into a type variable
 */
#define IOMUX_GPIO_ONLY		BIT(0)
#define IOMUX_WIDTH_4BIT	BIT(1)
#define IOMUX_SOURCE_PMU	BIT(2)
#define IOMUX_UNROUTED		BIT(3)

/**
 * @type: iomux variant using IOMUX_* constants
 * @offset: if initialized to -1 it will be autocalculated, by specifying
 *	    an initial offset value the relevant source offset can be reset
 *	    to a new value for autocalculating the following iomux registers.
 */
struct rockchip_iomux {
	int				type;
	int				offset;
};

/**
 * @reg_base: register base of the gpio bank
 * @reg_pull: optional separate register for additional pull settings
 * @clk: clock of the gpio bank
 * @irq: interrupt of the gpio bank
 * @pin_base: first pin number
 * @nr_pins: number of pins in this bank
 * @name: name of the bank
 * @bank_num: number of the bank, to account for holes
 * @iomux: array describing the 4 iomux sources of the bank
 * @valid: are all necessary informations present
 * @of_node: dt node of this bank
 * @drvdata: common pinctrl basedata
 * @domain: irqdomain of the gpio bank
 * @gpio_chip: gpiolib chip
 * @grange: gpio range
 * @slock: spinlock for the gpio bank
 */
struct rockchip_pin_bank {
	void 			*reg_base;
	int				irq;
	int				pin_base;
	int				nr_pins;
	char			*name;
	int				bank_num;
	struct rockchip_iomux		iomux[4];
	int				valid;
	int				toggle_edge_mode;
	void			*reg_mapped_base;
};

struct rockchip_pin_ctrl {
	struct rockchip_pin_bank	*pin_banks;
	unsigned int	nr_banks;
	unsigned int	nr_pins;
	char			*label;
	int             grf_mux_offset;
	int             pmu_mux_offset;
	void 			*grf_base;
	void 			*pmu_base;
	void 			*grf_mapped_base;
	void 			*pmu_mapped_base;
};

#define PIN_BANK(id, addr, pins, label)			\
	{						\
		.bank_num	= id,			\
		.reg_base	= (void *)addr,		\
		.nr_pins	= pins,			\
		.name		= label,		\
		.iomux		= {			\
			{ .offset = -1 },		\
			{ .offset = -1 },		\
			{ .offset = -1 },		\
			{ .offset = -1 },		\
		},					\
	}

#define PIN_BANK_IOMUX_FLAGS(id, addr, pins, label, iom0, iom1, iom2, iom3)	\
	{								\
		.bank_num	= id,					\
		.reg_base	= (void *)addr,			\
		.nr_pins	= pins,					\
		.name		= label,				\
		.iomux		= {					\
			{ .type = iom0, .offset = -1 },			\
			{ .type = iom1, .offset = -1 },			\
			{ .type = iom2, .offset = -1 },			\
			{ .type = iom3, .offset = -1 },			\
		},							\
	}


#ifndef __raw_readl
static inline unsigned int __raw_readl(const volatile void *addr)
{
	return *(const volatile unsigned int *) addr;
}
#endif

#define readl(addr) __raw_readl(addr)

#ifndef __raw_writel
static inline void __raw_writel(unsigned int b, volatile void *addr) 
{
	*(volatile unsigned int *) addr = b;
}
#endif

#define writel(b,addr) __raw_writel(b,addr)

int rockchip_gpio_init(void);
int rockchip_gpio_input(unsigned int pin);
int rockchip_gpio_output(unsigned int pin, unsigned int val);
int rockchip_gpio_set_mux(unsigned int pin, unsigned int mux);
int rockchip_gpio_get_mux(unsigned int pin);
int rockchip_gpio_pullup(unsigned int pin, unsigned int pull);

#endif /* _GPIO_LIB_H_ */
