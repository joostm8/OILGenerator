class OS:

    def __init__(self, trampoline_path="../../../..", app_source="default.cpp", prog_filename="defaultAppName", libraries=[]):
        self.trampoline_path = trampoline_path
        self.app_source = app_source
        self.prog_filename = prog_filename
        self.libraries = libraries

    def oil_representation(self):
        oil_repr = ("\tOS OSConfig {\n" +
                    "\tSTATUS = STANDARD;\n" +
                    "\tBUILD = TRUE {\n" +
                    '\tTRAMPOLINE_BASE_PATH = "' + self.trampoline_path + '";\n' +
                    '\tAPP_NAME = "' + self.prog_filename + '";\n' +
                    '\tAPP_SRC = "' + self.app_source + '";\n' +
                    "\tCPPCOMPILER = \"avr-g++\";\n" +
                    "\tCOMPILER =  \"avr-gcc\";\n" +
                    "\tLINKER = \"avr-gcc\";\n" +
                    "\tASSEMBLER = \"avr-gcc\";\n" +
                    "\tCOPIER = \"avr-objcopy\";\n" +
                    "\tSYSTEM = PYTHON;\n\n")

        for lib in self.libraries:
            oil_repr += ("\tLIBRARY = " + lib + ";\n")

        oil_repr += "\t};\n};\n\n"

        return oil_repr
