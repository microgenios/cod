CONTIKI_PROJECT = settings-example
all: $(CONTIKI_PROJECT)
CFLAGS += -DCONTIKI_CONF_SETTINGS_MANAGER=1
CONTIKI=$(shell targetos)/contiki
CONTIKI_WITH_RIME = 1
include $(CONTIKI)/Makefile.include
