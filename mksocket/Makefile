ROOTDIR   := ./
SRCDIR   := $(ROOTDIR)src/
OBJDIR   := $(ROOTDIR)build/
BINDIR   := $(ROOTDIR)bin/
NAME     := mksocket
CC_NAMES := mksocket.c
BINARY   := $(BINDIR)$(NAME)
all: binary

# Everything below this point is generic and could be put into a common 
# make include file to be included in other makefiles.

SFILES   := c
OFILES   := o
CC       := gcc
CFLAGS   := -c -Wall

SOURCES := $(foreach sname, $(CC_NAMES), $(SRCDIR)$(sname))
OBJECTS := $(patsubst $(SRCDIR)%.$(SFILES), $(OBJDIR)%.$(OFILES), $(SOURCES))

ALLFILES := $(SOURCES)

.PHONY: all clean binary

binary:    $(BINARY)

$(BINARY): $(OBJECTS)
		mkdir -p $(dir $@)
	        $(CC) $^ -o $@

$(OBJDIR)%$(OFILES):    $(SRCDIR)%$(SFILES)
		mkdir -p $(dir $@)
	        $(CC) $(CFLAGS) $< -o $@

clean:
	        rm -rf $(OBJDIR) $(BINDIR)

  
