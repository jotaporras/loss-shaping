import torch
import wandb


# importing the module
import json
  
# declaringa a class
class obj:
     
    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)
  
def dict2obj(dict1):
     
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict1), object_hook=obj)

class Dict2Obj(object):
    """
    Utility to turn wandb config dictionary into an object.
    """
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

def load_model(wandb_workspace,wandb_project,run_id):
    """
    Loads a model from a previously saved checkpoint.
    """
    api = wandb.Api()
    full_run_spec=f"{wandb_workspace}/{wandb_project}/{run_id}"
    run = api.run(full_run_spec)
    config = run.config
    model_name = config["model"]
    # Reflection to the class name
    MODEL_CLASS = getattr(__import__("models", fromlist=[model_name]), model_name)
    config_obj = Dict2Obj(config)
    model = MODEL_CLASS.Model(config_obj)

    wandb.restore("best_model.pth",full_run_spec,replace=True)

    # Now load the weights. They are expected to be in "checkpoint.pth" in the run directory.
    model.load_state_dict(torch.load("best_model.pth"))
    return model, dict2obj(config)
