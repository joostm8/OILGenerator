import xml.etree.ElementTree as et
from OILobjects import *
import textwrap


class SimulinkToOIL:

    def __init__(self, file_name):
        self.tree = et.parse(file_name)

    def generate_oil_file(self):
        # navigating down to our blocks and lines
        # Blocks are needed to get all data
        # lines are needed to find the link between trigger and ISR/Task
        root = self.tree.getroot()
        model = root.find('Model')
        system = model.find('System')
        blocks = system.findall('Block')
        lines = system.findall('Line')

        # lists and couple of params which will contain tasks and ISRs
        tasks = []
        isrs = []
        alarms = []
        resources = []

        # iterate over all blocks, find XML OIL objects, create OIL objects, add to lists above
        for block in blocks:
            #couple of params we need every loop
            block_type = None
            name = None
            period = None
            activation = 1
            auto_start = False
            priority = None
            schedule = None
            name = block.get('Name')
            obj = block.find('Object')
            if not(obj is None):
            #indexed access since name is always first
                block_type = obj[0].text
                if not(block_type is None) and 'tmpl' in block_type:
                    parameters = obj.find('Array')
                    if not(parameters is None):
                        for parameter in parameters:
                            # indexed access from here as these objects follow the same notation
                            if parameter[1].text == 'priorityNr' :
                                priority = parameter[3].text
                            elif parameter[1].text == 'period' :
                                period = parameter[3].text
                            elif parameter[1].text == 'maxActivation' :
                                activation = parameter[3].text
                            elif parameter[1].text == 'preemptable' :
                                schedule = 'FULL' if parameter[3].text == 'on' else 'NON'
                            elif parameter[1].text == 'generateAtStart' :
                                auto_start = True if parameter[3].text == 'on' else False
                        # All parameters set, now we create the OILobject dependent on block_type
                        if not(block_type is None):
                            #in is Python's "contains"
                            if 'Task' in block_type and 'tmpl' in block_type and not('Processor' in block_type or 'Queue' in block_type):
                                task = Task(name=name, priority=priority, auto_start=auto_start,
                                                       activation=activation, schedule=schedule)
                                print(task.oil_representation())
                                tasks.append(task)
                                if 'Periodic' in block_type:
                                    # In case of periodic task, automatically associate alarm
                                    alarm = Alarm(name=name+"Alarm", action_link=name, auto_start=auto_start,
                                                  alarm_time=period*1000, cycle_time=period*1000)
                                    print(alarm.oil_representation())
                                    alarms.append(alarm)

                            elif 'ISR' in block_type and 'tmpl' in block_type and not('Queue' in block_type):
                                if 'Periodic' in block_type:
                                    # periodic ISR, requires different treatment, do later
                                    pass
                                elif 'Triggered' in block_type:
                                    #triggered ISR, thus we must find the trigger
                                    trigger = "DEFAULT"
                                    for line in lines:
                                        # first check if this line connects to the current task
                                        if line[3].text == name:
                                            # then make sure the DstPort is 1
                                            if line[4].text == '1':
                                                # This means sth is connected to the trigger port. The name of this block
                                                # will be used as the trigger source
                                                trigger = line[1].text
                                    isr = ISR(name=name, priority=priority, source=trigger)
                                    print(isr.oil_representation())
                                    isrs.append(isr)

        #all isrs, tasks and accompanying alarms are read now, lets now create OS obj
        #small libraries added as test
        libraries = ['matlab', 'spi']
        os = OS(prog_filename='first_autogen_woo', libraries=libraries)

        #All good to go now! Creating oil file.
        oil_file = ("/* Running the following example:\n\
                      * just call goil a first time using the command line:\n\
                      * goil --target=avr/arduino/mega --templates=../../../../goil/templates/ file_name_placeholder.oil\n\
                      * /\n\n" +
                    "OIL_VERSION = \"2.5\" : \"test\";\n\n" +
                    "CPU test {\n")
        oil_file_body = os.oil_representation()
        oil_file_body += "APPMODE stdAppmode {DEFAULT = TRUE;};\n\n"
        for alarm in alarms:
            oil_file_body += alarm.oil_representation()
        for task in tasks:
            oil_file_body += task.oil_representation()
        for isr in isrs:
            oil_file_body += isr.oil_representation()
        #oil_file_body = textwrap.indent(oil_file_body, '\t')
        oil_file += oil_file_body
        oil_file += "};"

        #all ready to write out now
        final_file = open('default.oil', 'w')
        final_file.write(oil_file)
        final_file.close()
