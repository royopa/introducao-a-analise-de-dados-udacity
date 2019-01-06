import unicodecsv
from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object. 
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)


def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)


def get_unique_students(table_list, field_name='account_key'):
    unique_list = set()
    for row in table_list:
        unique_list.add(row[field_name])
    return unique_list


enrollments = read_csv('./data/enrollments.csv')
daily_engagement = read_csv('./data/daily_engagement.csv')
project_submissions = read_csv('./data/project_submissions.csv')


# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    
enrollments[0]


# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    
daily_engagement[0]


# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

project_submissions[0]


enrollment_num_rows = len(enrollments)
enrollment_unique_students = get_unique_students(enrollments)
enrollment_num_unique_students = len(enrollment_unique_students)
for row in daily_engagement:
    row['account_key'] = row['acct']
    del[row['acct']]

engagement_num_rows = len(daily_engagement)
engagement_unique_students = get_unique_students(daily_engagement, 'account_key')
engagement_num_unique_students = len(engagement_unique_students)


submission_num_rows = len(project_submissions)
submission_unique_students = get_unique_students(project_submissions)
submission_num_unique_students = len(submission_unique_students)

for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in engagement_unique_students:
        print(enrollment)
        break


num_problem_students = 0
for enrollment in enrollments:
    student = enrollment['account_key']
    if (student not in engagement_unique_students and 
            enrollment['join_date'] != enrollment['cancel_date']):
        num_problem_students += 1

print(num_problem_students)

udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
print(len(udacity_test_accounts))


def remove_udacity_accounts(data, udacity_test_accounts):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

non_udacity_enrollments = remove_udacity_accounts(enrollments, udacity_test_accounts)
non_udacity_engagement =  remove_udacity_accounts(daily_engagement, udacity_test_accounts)
non_udacity_submissions =  remove_udacity_accounts(project_submissions, udacity_test_accounts)

print(enrollment_num_rows, enrollment_num_unique_students, len(non_udacity_enrollments))
print(engagement_num_rows, engagement_num_unique_students, len(non_udacity_engagement))
print(submission_num_rows, submission_num_unique_students, len(non_udacity_submissions))

paid_students = {}

for enrollment in non_udacity_enrollments:
    if enrollment['days_to_cancel'] is None or enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        paid_students[account_key] = enrollment_date

        if account_key not in paid_students or \
                enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date


print(len(paid_students))

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7


#####################################
#                 7                 #
#####################################

## Create a list of rows from the engagement table including only rows where
## the student is one of the paid students you just found, and the date is within
## one week of the student's join date.

paid_engagement_in_first_week = []



