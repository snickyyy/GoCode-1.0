from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int
from six import text_type


class TokenRegisterGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


class EmailChangeTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.password)

    # def check_token(self, user, token):
    #     """
    #     Check that a password reset token is correct for a given user.
    #     """
    #     if not (user and token):
    #         print("if not (user and token): eror")
    #         return False
    #     # Parse the token
    #     try:
    #         ts_b36, _ = token.split("-")
    #     except ValueError:
    #         print(f"\n\n\n\nerror ts_b36, _ = token.split("")")
    #         return False
    #
    #     try:
    #         ts = base36_to_int(ts_b36)
    #     except ValueError:
    #         print("error ts = base36_to_int(ts_b36)")
    #         return False
    #
    #     # Check that the timestamp/uid has not been tampered with
    #     for secret in [self.secret, *self.secret_fallbacks]:
    #         if constant_time_compare(
    #             self._make_token_with_timestamp(user, ts, secret),
    #             token,
    #         ):
    #             print("\n\n\n\good if constant_time_compare(")
    #             break
    #     else:
    #         print("cycle")
    #         return False
    #
    #     # Check the timestamp is within limit.
    #     if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
    #         print("\n\n\n\ntimeout")
    #         return False
    #
    #     return True
