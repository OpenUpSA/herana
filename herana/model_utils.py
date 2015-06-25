from django.utils.translation import ugettext_lazy as _

YESNO = (
    ('Y', _('Yes')),
    ('N', _('No')),
)

FOCUS_AREAS = (
    (1, _('Teaching and learning')),
    (2, _('Research')),
    (3, _('Service (Professional Discipline-Based)')),
    (4, _('Other'))
)

CLASSIFICATION = (
    (1, _('Project')),
    (2, _('Programme')),
    (3, _('Service')),
    (4, _('Other'))
)

INITIATION_STATEMENTS = (
    (1, _('Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project')),
    (2, _('Informed by the university research or contracts office about the reach project')),
    (3, _('Initiated by colleagues at own university')),
    (4, _('Initiated by project leader')),
    (5, _('Initiated by project leader in collaboration with colleagues')),
    (6, _('Follow-on or continuation from existing project')),
    (7, _('Project assigned to project leader')),
)

NUMBER_AUTHORS = (
    (1, _('One author')),
    (1, _('More than one author'))
)

ADV_GROUP_FREQ = (
    (1, _('Monthly')),
    (2, _('Quarterly')),
    (3, _('Annually')),
    (4, _('Ad hoc'))
)

INITIATIVE_PARTIES = (
    (1, _('A third party has been contracted to develop the product / service / intervention / policy')),
    (2, _('The project team will develop the product / service / intervention / policy')),
    (3, _('Other')),
)

RESEARCH_CLASSIFICATION = (
    (1, _('The project conducted original research')),
    (2, _('The project collected new data and conducted original research to complete the project')),
    (3, _('The project collected new data and applied existing knowledge to the data collected to complete the project')),
    (4, _('No new data was required and existing knowledge was applied to complete the project')),
    (5, _('Not applicable'))
)

RECORD_STATUS = (
    (1, 'Incomplete'),
    (2, 'Final'),
    (3, 'Rejected')
)
