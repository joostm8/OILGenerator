class Event:

    def __init__(self, mask="AUTO"):
        self.mask = mask

    def oil_representation(self):
        oil_repr = ("EVENT Event1 {\n" +
                    "\tMASK = " + self.mask + ";\n" +
                    "};\n\n")

        return oil_repr
