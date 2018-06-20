class Task:

    def __init__(self, name="default", priority=5, auto_start=False, activation=1, schedule="FULL", stack=512, event=False, resources = []):
        self.name = name
        self.priority = priority
        self.auto_start = auto_start
        self.activation = activation
        self.schedule = schedule
        self.stack = stack
        self.event = event
        self.resources = resources

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
                     "\tSTACKSIZE = " + str(self.stack) + ";\n")
        if self.event:
            oil_repr += "\tEVENT = EVENT1;\n"

        for resource in self.resources:
            oil_repr += "\tRESOURCE = " + resource.name + ";\n"

        oil_repr += "};\n\n"

        return oil_repr

    def c_representation(self):
        c_repr = ("TASK(" + self.name + "){\n" +
                  "/* Insert Input mapping code here */\n\n" +
                  "/* Step the code executed by this TASK here*/\n\n" +
                  "/* Insert Output mapping here */\n\n" +
                  "}\n"
                  )

        return c_repr
