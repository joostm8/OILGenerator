class Alarm:

    def __init__(self, name="default", counter="SystemCounter", action="ACTIVATETASK", action_link="default", auto_start=False, alarm_time=0, cycle_time=0):
        self.name = name
        self.counter = counter
        self.action = action
        self.action_link = action_link
        self.auto_start = auto_start
        self.alarm_time = alarm_time
        self.cycle_time = cycle_time

    def oil_representation(self):
        oil_repr = ("ALARM " + self.name + " {\n" +
                    "\tCOUNTER = " + self.counter + ";\n" +
                    "\tACTION = " + self.action + " {\n" +
                    "\t\tTASK = " + self.action_link + ";\n\t};\n")

        if self.auto_start:
            oil_repr += ("\tAUTOSTART = TRUE {\n" +
                         "\tALARMTIME = " + str(self.alarm_time) + ";\n" +
                         "\tCYCLETIME = " + str(self.cycle_time) + ";\n" +
                         "\tAPPMODE = stdAppmode;\n\t};\n")
        else:
            oil_repr += "\tAUTOSTART = FALSE;\n"

        oil_repr += "};\n\n"

        return oil_repr
