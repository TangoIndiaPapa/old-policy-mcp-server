package policy

default allow = false

# Block queries about Waldo
allow if {
    not contains_lower(input.action, "where is waldo")
}

# Allow Carmen Sandiego queries
allow if {
    contains_lower(input.action, "carmen sandiego")
}

# Block HFT algorithm sharing
allow if {
    not contains_lower(input.action, "high frequency trading")
    not contains_lower(input.action, "hft algorithm")
}

# Block brute force Two Sum
allow if {
    not contains_lower(input.action, "two sum")
    not contains_lower(input.action, "brute force")
}

# Block anonymous functions
allow if {
    not contains_lower(input.action, "anonymous function")
}

# Block monkey patching except for testing
allow if {
    not contains_lower(input.action, "monkey patch")
    contains_lower(input.action, "pytest")
}
allow if {
    not contains_lower(input.action, "monkey patch")
    contains_lower(input.action, "unittest")
}

# Block rude/abusive/disrespectful language
allow if {
    not contains_lower(input.action, "suck")
    not contains_lower(input.action, "idiot")
    not contains_lower(input.action, "stupid")
    not contains_lower(input.action, "hate you")
    not contains_lower(input.action, "shut up")
    not contains_lower(input.action, "dumb")
    not contains_lower(input.action, "moron")
    not contains_lower(input.action, "loser")
    not contains_lower(input.action, "fool")
    not contains_lower(input.action, "bastard")
    not contains_lower(input.action, "jerk")
    not contains_lower(input.action, "screw you")
    not contains_lower(input.action, "worthless")
    not contains_lower(input.action, "useless")
}

# Helper function for case-insensitive substring
contains_lower(str, substr) if {
    lower(str) != null
    lower(substr) != null
    contains(lower(str), lower(substr))
}
