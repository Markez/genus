import logging, json, string
from random import choice, randint
from decouple import config
from apps.alpha.models import Chama, plan_packages
from backend.common.processes import record_user_activity
from apps.common.models import userActivities
from apps.accounts.models import profile
from django.contrib.auth.models import User


logging = logging.getLogger('chama_backend')


class ChamaBaseHandler:
    @staticmethod
    def new_chama_registration(creator, name, year_founded, maximum_members, description, contribution_intervals,
                               total_contributions, saved_amounts, twitter_link, facebook_link, plan):
        prof = profile.objects.get(username_id=creator.id)
        creator_number = prof.mobile_number
        try:
            data = Chama()
            data.creator = creator.username
            data.mobile_number = creator_number
            data.name = name
            data.year_founded = year_founded
            data.maximum_members = maximum_members
            data.description = description
            data.contribution_intervals = ChamaBaseHandler.chama_intervals(contribution_intervals)
            data.total_contributions = total_contributions
            data.saved_amounts = saved_amounts
            data.twitter_link = twitter_link
            data.facebook_link = facebook_link
            data.plan_package = ChamaBaseHandler.chama_palns(plan)
            data.save()
            record_user_activity(userActivities.CREATE_CHAMA, creator_number, userActivities.COMPLETED)
            return True
        except Exception as e:
            logging.info(e)
            return False

    @staticmethod
    def chama_intervals(contribution_intervals):
        if contribution_intervals == "daily":
            interval = Chama.DAILY
        elif contribution_intervals == "weekly":
            interval = Chama.WEEKLY
        elif contribution_intervals == "monthly":
            interval = Chama.MONTHLY
        else:
            interval = Chama.YEARLY
        return interval

    @staticmethod
    def chama_palns(plan):
        if plan == "platinum":
            pack = Chama.PLATINUM
        elif plan == "silver":
            pack = Chama.SILVER
        elif plan == "bronze":
            pack = Chama.BRONZE
        elif plan == "starter":
            pack = Chama.STARTER
        else:
            pack = Chama.FREE
        return pack


class ChamaPackagesHandler:
    @staticmethod
    def get_plan_packages():
        free = plan_packages.objects.get(slug="free")
        starter = plan_packages.objects.get(slug="starter")
        silver = plan_packages.objects.get(slug="silver")
        platinum = plan_packages.objects.get(slug="platinum")
        context = {
            'free': free,
            'starter': starter,
            'silver': silver,
            'platinum': platinum
        }
        return context
