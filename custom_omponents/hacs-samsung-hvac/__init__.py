DOMAIN = "hello_state"


def setup(hass, config):
    print("Hello from the hello_state custom component!")
    hass.states.set("hello_state.world", "Paulus")

    # Return boolean to indicate that initialization was successful.
    return True