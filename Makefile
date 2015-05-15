TARGET=thumbv7m-none-eabi
PLATFORM=stm32f4
EXAMPLE_NAME=blink_stm32f4
OBJCOPY=arm-none-eabi-objcopy
OBJDUMP=arm-none-eabi-objdump

PLATFORM_DIR=src/hal/$(PLATFORM)
LINK_SCRIPT=$(PLATFORM_DIR)/layout.ld

LDFLAGS=-mthumb -mcpu=cortex-m3 -T$(LINK_SCRIPT) -lm -lgcc -v

EXAMPLE_FILE=target/$(TARGET)/release/examples/$(EXAMPLE_NAME)

.PHONY: build clean listing
build: $(EXAMPLE_NAME).bin

clean:
	-rm *.bin
	-rm *.lst
	cargo clean

listing: $(EXAMPLE_NAME).lst

$(EXAMPLE_FILE):
	cargo rustc --example blink_stm32f4 --release --target=$(TARGET) --verbose -- -C link-args="$(LDFLAGS)"

$(EXAMPLE_NAME).bin: $(EXAMPLE_FILE)
	$(OBJCOPY) -O binary $< $@

$(EXAMPLE_NAME).lst: $(EXAMPLE_FILE)
	$(OBJDUMP) -D $< > $@
