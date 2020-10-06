import functools

RULE_NAME = 0
RULE_CALLBACK = 1

def validate_args(args, rules):
    if type(args) != dict:
        return False

    for rule in rules:
        if rule[RULE_NAME] not in args or not rule[RULE_CALLBACK](args[rule[RULE_NAME]]):
            return False

    return True

def validator(rules):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args):
            if validate_args(args, rules):
                return func(args)
            
            raise ValueError('Invalid request.')

        return wrapper

    return decorator
