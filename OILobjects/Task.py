class Task:

    def __init__(self, name="default", priority=5, auto_start=False, activation=1, schedule="FULL", stack=512):
        self.name = name
        self.priority = priority
        self.auto_start = auto_start
        self.activation = activation
        self.schedule = schedule
        self.stack = stack

    def oil_representation(self):
        oil_repr = ("TASK " + self.name + " {\n" +
                    "\tPRIORITY = " + str(self.priority) + ";\n")
        if self.auto_start:
            oil_repr += ("\tAUTOSTART = TRUE {\n" +
                         "\t\tAPPMODE = stdAppmode;\n" +
                         "\t};")
        else:
            oil_repr += "\tAUTOSTART = FALSE;\n"

        oil_repr += ("\tACTIVATION = " + str(self.activation) + ";\n" +
                     "\tSCHEDULE = " + self.schedule + ";\n" +
                     "\tSTACKSIZE = " + str(self.stack) + ";\n};\n\n")

        return oil_repr
