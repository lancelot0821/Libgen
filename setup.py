import subprocess
import os


def set_workspace(workplace):
    if os.path.exists(workplace)==False:
        os.makedirs(workplace)
        os.makedirs(os.path.join(workplace, 'sirius_workspace'))
        os.makedirs(os.path.join(workplace, 'sirius_workspace','opt'))
        os.makedirs(os.path.join(workplace, 'temp_data'))
        os.makedirs(os.path.join(workplace, 'temp_data','msms'))
    else:
        print("the workspace exists!")


print("i am setup functions!!")
