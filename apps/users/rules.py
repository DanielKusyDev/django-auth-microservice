import rules
from rules import predicate


@predicate
def is_account_owner(user, obj):
    return user.pk == obj.pk


rules.add_perm('is_staff', rules.is_staff)
rules.add_perm('is_account_owner', is_account_owner)
rules.add_perm('users.delete', rules.is_staff | is_account_owner)
rules.add_perm('allow_any', rules.always_allow)
