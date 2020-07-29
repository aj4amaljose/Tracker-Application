"""
Main module
"""
import argparse
from tracker.tracker import get_initial_persons, load_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', dest='operation', required=True)
    parser.add_argument('-p', '--Path', dest='path', required=False)
    parser.add_argument('-i', '--patientId', dest='patient_id', required=False)
    parser.add_argument('-d', '--days', dest='days', required=False)
    args = parser.parse_args()
    if args.operation == 'load':
        if not args.path:
            raise Exception("Please provide Directory path as '-p <path>'in arguments")
        else:
            load_data.load_files_in_a_folder(args.path)
    elif args.operation == 'get':
        if not args.patient_id:
            raise Exception("Please provide Patient Social No as -'i <Social No>' in arguments")
        else:
            if not args.days:
                days = 0
            else:
                days = int(args.days)
            track = get_initial_persons.TrackerHelper(person_id=args.patient_id, no_of_days=days)
            print(track.get_persons_related)
            # track.get_visualisation() # Add visualization
    else:
        raise Exception("Invalid Option")



