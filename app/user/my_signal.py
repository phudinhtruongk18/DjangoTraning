# from django import dispatch

# some_task_done = dispatch.Signal()


# def do_some_task(sender='phu',instance="â", created="created", *args, **kwargs):
# 	# did some thing
#     print("Fuk")
#     some_task_done.send(sender='phu',instance="â", created="created", *args, **kwargs)

# from django.dispatch import receiver

# @receiver(some_task_done)
# def my_task_done(sender, **kwargs):
#     print(sender)

# my_task_done(sender="main")