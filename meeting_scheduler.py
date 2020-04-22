# Conference room scheduling.

import sys

class MeetingScheduler(object):
    """docstring for MeetingScheduler"""

    def __init__(self, input_file, input_args):
        self.rooms_details = self._load_room_details(input_file)
        self.no_of_team_member = int(input_args[0])
        self.floor_number = int(input_args[1])
        self.meeting_start_time = input_args[2]
        self.meeting_end_time = input_args[3]

    def _load_room_details(self, input_file):
        self.rooms_details = {}
        for room in input_file.readlines():
            details = room.strip().split(",")
            floor, room = int(details[0].split(".")[0]), int(
                details[0].split(".")[1])
            self.rooms_details[floor, room] = {
                'capacity': int(details[1]),
                'time_slots': details[2:]
            }
        return self.rooms_details
        #{(floor, room): {capacity, time_slots}, ...}

    @staticmethod
    def find_available_slot(slots_list, slot):
        slots = [(slot1, slot2) for slot1, slot2 in zip(slots_list[::2], slots_list[1::2])] 
        for slot_start_time, slot_end_time in slots:
            if (slot[0] >= slot_start_time) and (slot[1] <= slot_end_time):
                return {'start_time': slot_start_time, 'end_time': slot_end_time}
        return None

    @staticmethod
    def get_slot_duraion(satrt_slot, end_slot):
        # in minutes
        slot_end_minutes = int(end_slot.split(":")[0]) * 60 + int(end_slot.split(":")[1])
        slot_start_minutes = int(satrt_slot.split(":")[0]) * 60 + int(satrt_slot.split(":")[1])
        return slot_end_minutes - slot_start_minutes

    def find_room(self):
        size_matched = False
        room_identified = {}
        for (floor, room), room_details in self.rooms_details.items():
            if self.no_of_team_member <= room_details['capacity']:
                size_matched = True
                matched_slot = self.find_available_slot(
                                slots_list=room_details['time_slots'], 
                                slot=(self.meeting_start_time, self.meeting_end_time)
                            )
                if matched_slot:
                    slot_duration_of_input = self.get_slot_duraion(self.meeting_start_time, self.meeting_end_time)
                    slot_duration_of_matched = self.get_slot_duraion(matched_slot['start_time'], matched_slot['end_time'])
                    slot_extra_time = slot_duration_of_matched - slot_duration_of_input # to know more close availibilty

                    if not room_identified:
                        room_identified['floor'] = floor
                        room_identified['room'] = room
                        room_identified['slot'] = matched_slot
                        room_identified['slot_extra_time'] = slot_extra_time
                    else:
                        if abs(self.floor_number - floor) < abs(self.floor_number - room_identified['floor']):
                            room_identified['floor'] = floor
                            room_identified['room'] = room
                            room_identified['slots'] = matched_slot
                            room_identified['slot_extra_time'] = slot_extra_time
                        elif abs(self.floor_number - floor) == abs(self.floor_number - room_identified['floor']):
                            if slot_extra_time < room_identified['slot_extra_time']:
                                room_identified['floor'] = floor
                                room_identified['room'] = room
                                room_identified['slots'] = matched_slot
                                room_identified['slot_extra_time'] = slot_extra_time

        if not size_matched:
            return "team members are more compare to available capacity of room/slots"
        result = ""
        if room_identified.get('floor'):
            result = str(room_identified['floor']) + "." + str(room_identified['room'])

        return result


def verify_inputs(inputs):
    try:
        int(inputs[0])
    except ValueError:
        print("Invalid team number!")
        return False

    try:
        int(inputs[1])
    except ValueError:
        print("Invalid floor number!")
        return False

    try:
        int(inputs[2].split(":")[0])
        int(inputs[2].split(":")[1])
    except Exception:
        print("Invalid meeitng start time!")
        return False

    try:
        int(inputs[3].split(":")[0])
        int(inputs[3].split(":")[1])
    except Exception:
        print("Invalid meeitng end time!")
        return False
    return True


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        try:
            input_file = open(sys.argv[1])
        except FileNotFoundError:
            print("File not found, please provide correct file path!")
        else:
            input_args = sys.argv[2].split(",")
            if len(input_args) == 4:
                #=============MAIN==============#
                if verify_inputs(input_args):
                    ms = MeetingScheduler(input_file, input_args)
                    room = ms.find_room()
                    print(room)
                #===============================#
            else:
                print("meeting inputs '%s' are not good!" % sys.argv[2])

    else:
        print("Not enough arguments to pasred!")
