class ISR:

    def __init__(self, name="default", category=2, priority=0, stack=512, source="DEFAULT"):
        self.name = name
        self.category = category
        self.priority = priority
        self.stack = stack
        self.source = source

    def oil_representation(self):
        oil_repr = ("ISR " + self.name + "{\n" +
                    "\tCATEGORY = " + str(self.category) + ";\n" +
                    "\tPRIORITY = " + str(self.priority) + ";\n" +
                    "\tSTACKSIZE = " + str(self.stack) + ";\n" +
                    "\tSOURCE = " + self.source + ";\n};\n\n")
        return oil_repr
