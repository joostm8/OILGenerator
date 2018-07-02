import xml.etree.ElementTree as et
from OILobjects import *
import datetime

class SimulinkToOIL:

    def __init__(self, file_name):
        self.tree = et.parse(file_name)

    def generate_files(self):
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
        events = []

        # iterate over all blocks, find XML OIL objects, create OIL objects, add to lists above
        for block in blocks:
            #couple of params we need every loop
            block_type = None
            name = None
            period = None
            activation = 1
            auto_start = False
            generate_at_start = None
            priority = None
            schedule = None
            event = None
            alarm_time = None
            cycle_time = None
            requiredResources = []
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
                                generate_at_start = True if parameter[3].text == 'on' else False
                            elif parameter[1].text == 'requiresEvent':
                                event = True if '1' in parameter[3].text else False
                            elif parameter[1].text == 'requiresResource':
                                tempList = eval(parameter[3].text.replace(' ', ','))
                                for i in tempList:
                                    if i > 0:
                                        requiredResources.append(Resource(name = "Resource"+str(i)))
                            elif parameter[1].text == 'alarmTime':
                                alarm_time = parameter[3].text
                            elif parameter[1].text == 'cycleTime':
                                cycle_time = parameter[3].text
                            elif parameter[1].text == 'autoStart':
                                auto_start = True if parameter[3].text == 'on' else False
                        # All parameters set, now we create the OILobject dependent on block_type
                        if not(block_type is None):
                            #in is Python's "contains"
                            if not(event is None) and event == True and not events:
                                event1 = Event()
                                events.append(event1)
                            if requiredResources:
                                for requiredResource in requiredResources:
                                        exists = False
                                        for resource in resources:
                                            # check if the resource already exists.
                                            if requiredResource == resource:
                                                exists = True
                                        if not exists:
                                            resources.append(requiredResource)
                            if 'Task' in block_type and 'tmpl' in block_type and not('Processor' in block_type or 'Queue' in block_type):
                                task = Task(name=name, priority=priority, generate_at_start=generate_at_start,
                                                       activation=activation, schedule=schedule, event=event if not(event is None) else False, resources = requiredResources)
                                print(task.oil_representation())
                                tasks.append(task)
                                if 'Periodic' in block_type:
                                    # In case of periodic task, automatically associate alarm
                                    alarm = Alarm(name=name+"Alarm", action_link=name, auto_start=True,
                                                  alarm_time=int(float(period)*1000), cycle_time=int(float(period)*1000))
                                    print(alarm.oil_representation())
                                    alarms.append(alarm)

                            elif 'ISR' in block_type and 'tmpl' in block_type and not('Queue' in block_type):
                                if 'Periodic' in block_type:
                                    # periodic ISR, is a simplification which means the periodic
                                    # interrupt source does not need to be connected
                                    # contrary to triggered, we cannot deduce the name
                                    # thus we opt for default.
                                    trigger = "PERIODIC_TRIG_PLACEHOLDER"
                                    isr = ISR(name=name, priority=priority, source=trigger, resources=requiredResources)
                                    print(isr.oil_representation())
                                    isrs.append(isr)
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
                                    isr = ISR(name=name, priority=priority, source=trigger, resources = requiredResources)
                                    print(isr.oil_representation())
                                    isrs.append(isr)
                            elif 'Alarm' in block_type and 'tmpl' in block_type:
                                # Separate alarms are also possible. If connected to a task they should activate that task.
                                # otherwise its an alarmcallback.
                                # for each line, search if we can find the current alarm.
                                # if connected to task, action is activateTask
                                # otherwise placeholder
                                for line in lines:
                                    # src_block
                                    if line[1].text == name:
                                        # this is the current task.
                                        # dest:
                                        destBlk = None
                                        for i in line:
                                            if i.get('Name') == 'DstBlock':
                                                destBlk = i.text
                                        #now we need to search through all blocks to find this block
                                        # if the type is tmpl_triggered_task we do activate task
                                        # otherwise placeholder
                                        for block2 in blocks:
                                            if(block2.get('Name') == destBlk):
                                                #found the block
                                                obj2 = block2.find('Object')
                                                if not(obj2 is None):
                                                    if 'tmpl_Triggered_Task' in obj2[0].text:
                                                        # is a triggered task
                                                        alarm = Alarm(name=name, action_link=destBlk,
                                                                      auto_start=auto_start,
                                                                      alarm_time=alarm_time,
                                                                      cycle_time=cycle_time)
                                                        print(alarm.oil_representation())
                                                        alarms.append(alarm)
                                                else:
                                                    alarm = Alarm(name=name, action="MANUAL_COMPLETE", action_link="MANUAL_COMPLETE",
                                                                  auto_start=auto_start,
                                                                  alarm_time=alarm_time,
                                                                  cycle_time=cycle_time)
                                                    print(alarm.oil_representation())
                                                    alarms.append(alarm)
        self.generate_oil_file(tasks, isrs, resources, events, alarms)
        self.generate_c_template(tasks, isrs)

    def generate_oil_file(self, tasks=[], isrs=[], resources=[], events=[], alarms=[]):
        # all isrs, tasks and accompanying alarms are read now, lets now create OS obj
        # small libraries added as test
        libraries = ['matlab']
        os = OS(prog_filename='programmingFile', libraries=libraries)

        # All good to go now! Creating oil file.
        oil_file = ("/*\n* This is a OIL file generated by OILGenerator by Joost Mertens \n"+
                    "* Generated on: " + str(datetime.datetime.now()) + "\n"+
                    "* just call goil a first time using the command line:\n"
                    "* goil --target=avr/arduino/mega --templates=../../../../goil/templates/ file_name_placeholder.oil\n"+
                    "*/\n\n" +
                    "OIL_VERSION = \"2.5\" : \"test\";\n\n" +
                    "CPU test {\n")
        oil_file_body = os.oil_representation()
        oil_file_body += "APPMODE stdAppmode {DEFAULT = TRUE;};\n\n"
        for event in events:
            oil_file_body += event.oil_representation()
        for resource in resources:
            oil_file_body += resource.oil_representation()
        for alarm in alarms:
            oil_file_body += alarm.oil_representation()
        for task in tasks:
            oil_file_body += task.oil_representation()
        for isr in isrs:
            oil_file_body += isr.oil_representation()
        # oil_file_body = textwrap.indent(oil_file_body, '\t')
        oil_file += oil_file_body
        oil_file += "};"

        # all ready to write out now
        final_file = open('default.oil', 'w')
        final_file.write(oil_file)
        final_file.close()

    def generate_c_template(self, tasks=[], isrs=[]):
        c_file = ("/**\n"
                  "* This is a template of C code generated by OILGenerator by Joost Mertens\n"
                  "* Generated on: " + str(datetime.datetime.now()) + "\n"
                  "* Directions are given concerning which code should be executed on which locations\n"
                  "* The final mapping is still user dependent.\n"
                  "**/\n\n")
        c_file += ("/* Includes are placed here, commonly used includes are already listed */\n"
                   '#include "Arduino.h"\n'
                   '#include <stddef.h>\n'
                   '#include <stdio.h>\n'
                   '#include <avr/io.h\n'
                   '\n')
        c_file += ("/* Include Matlab includes here */\n\n")
        c_file += ("#undef ISR //Remove AVR-GCC ISR version\n"
                   'extern "C"{\n'
                   '\t#include "tpl_app_config.h"\n'
                   '\t#include "tpl_os.h"\n'
                   '}\n\n')
        c_file += ("void setup(void){\n"
                   "/* Include all initialisations here */\n\n"
                   "}\n\n")
        for task in tasks:
            c_file += task.c_representation()
        for isr in isrs:
            c_file += isr.c_representation()
        c_file += ("/*\nEOF\n*/")

        final_file = open('default.c', 'w')
        final_file.write(c_file)
        final_file.close()
