# TODO(mcoffin): derive TARGET from PLATFORM and EXAMPLE_NAME
TARGET=thumbv7m-none-eabi
STRIP=arm-none-eabi-strip
OBJCOPY=arm-none-eabi-objcopy
OBJDUMP=arm-none-eabi-objdump

PLATFORM_DIR=src/hal/$(PLATFORM)
LINK_SCRIPT=$(PLATFORM_DIR)/layout.ld

OUT_DIR=target/$(TARGET)/release
EXAMPLE_DIR=$(OUT_DIR)/examples
EXAMPLE_FILE=$(EXAMPLE_DIR)/$(EXAMPLE_NAME)

ISR_SRC=src/hal/isr.rs
ISR_CRATE=$(shell rustc --print crate-name $(ISR_SRC))
ISR_FILE=$(OUT_DIR)/$(ISR_CRATE).o

LDFLAGS=-mthumb -mcpu=cortex-m3 -T$(LINK_SCRIPT) -lm -lgcc $(ISR_FILE)

BIN_FILE=$(EXAMPLE_DIR)/$(EXAMPLE_NAME).bin
LST_FILE=$(EXAMPLE_DIR)/$(EXAMPLE_NAME).lst

.PHONY: build clean listing
build: $(BIN_FILE)

clean:
	-rm $(ISR_FILE)
	cargo clean

listing: $(OUT_DIR)/$(EXAMPLE_NAME).lst

$(EXAMPLE_FILE): $(ISR_FILE)
	cargo rustc --example $(EXAMPLE_NAME) --release --target=$(TARGET) --verbose -- -C link-args="$(LDFLAGS)"

$(BIN_FILE): $(EXAMPLE_FILE)
	$(OBJCOPY) -O binary $< $@

$(LST_FILE): $(EXAMPLE_FILE)
	$(OBJDUMP) -D $< > $@

$(ISR_FILE): $(ISR_SRC) | $(OUT_DIR)
	rustc --target=$(TARGET) --emit=obj --out-dir=$(OUT_DIR) --cfg mcu_$(PLATFORM) -C opt-level=2 $<
	$(STRIP) -N rust_begin_unwind -N rust_stack_exhausted -N rust_eh_personality $@

$(OUT_DIR):
	mkdir -p $@
