"""Constants."""

from startups_lk._utils import log

CACHE_NAME = 'startups_lk'
CACHE_TIMEOUT = 3600


def build_reverse_index(index):
    return dict(
        list(
            map(
                lambda x: [x[1], x[0]],
                index.items(),
            )
        )
    )


STARTUP_STAGES_INDEX = {
    'Unknown': 0,
    'Ideation': 1,
    'Traction': 2,
    'Break-Even': 3,
    'Profit': 4,
    'Scaling': 5,
    'Stable': 6,
}


def get_startup_stage_id(startup_stage):
    if startup_stage not in STARTUP_STAGES_INDEX:
        log.error(f'Unknown startup_stage: {startup_stage}')
    return STARTUP_STAGES_INDEX.get(startup_stage, 0)


FUNDING_STAGES_INDEX = {
    'Unknown': 0,
    'Pre-seed': 1,
    'Seed': 2,
    'Angel': 3,
    'Series A': 4,
    'Series B': 5,
    'Venture Capital': 6,
    'Mezzanine financing and bridge loans': 7,
    'Initial Public Offering': 8,
    'IPO (Initial Public Offering)': 8,
}


def get_funding_stage_id(funding_stage):
    if funding_stage not in FUNDING_STAGES_INDEX:
        log.error(f'Unknown funding_stage: {funding_stage}')
    return FUNDING_STAGES_INDEX.get(funding_stage, 0)


CATEGORY_TO_COLOR = {
    'Agricultural/ Agritech': 'darkgreen',
    'Artificial Intelligence': 'blue',
    'Arts & Culture': 'red',
    'Automotive': 'purple',
    'Cloud Computing': 'darkblue',
    'Computer Hardware': 'darkblue',
    'Construction': 'darkgray',
    'Consulting': 'gray',
    'Design & Print': 'red',
    'Digital Marketing': 'pink',
    'e-commerce': 'orange',
    'Educational/ Edutech': 'lightblue',
    'Electronics and Electrical': 'darkblue',
    'Entertainment': 'pink',
    'Events': 'pink',
    'Fashion': 'magenta',
    'Financial/Fintech': 'gold',
    'Food & Beverages': 'green',
    'Green Technology': 'darkgreen',
    'Human Resource': 'pink',
    'Internet of Things': 'darkblue',
    'IT Products': 'black',
    'IT Services': 'black',
    'Life Sciences': 'darkgreen',
    'Logistics': 'darkgray',
    'Machine Learning': 'blue',
    'Manufacturing': 'darkblue',
    'Media': 'pink',
    'Medical & Health/ Medtech': 'green',
    'Mobile Application': 'black',
    'Not for Profit': 'pink',
    'Other': 'gray',
    'Platforms': 'blue',
    'Power & Energy': 'darkblue',
    'Real Estate': 'gold',
    'Retail': 'orange',
    'Robotic Process Automation (RPA)': 'darkblue',
    'Robotics': 'darkblue',
    'Social Innovation': 'lightblue',
    'Sports': 'pink',
    'Telecommunication and Networking': 'darkblue',
    'Travel & Tourism': 'darkgreen',
    'UI / UX': 'black',
}
