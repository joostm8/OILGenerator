class Resource:

    def __init__(self, name="DEAFULT", resourceProperty="STANDARD"):
        self.name = name
        self.resourceProperty = resourceProperty

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def oil_representation(self):
        oil_repr = ("RESOURCE " + self.name + " {\n" +
                    "\tRESOURCEPROPERTY = " + self.resourceProperty + ";\n")
        oil_repr += "};\n\n"

        return oil_repr
