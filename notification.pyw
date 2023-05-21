from win11toast import toast
import Recall

info = Recall.active_recall() # data needed for question
icon_image ="https://images.pexels.com/photos/167682/pexels-photo-167682.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
icon_correct="https://images.unsplash.com/photo-1567578923208-5cc60003892d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
icon_incorrect="https://images.unsplash.com/photo-1512314889357-e157c22f938d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1471&q=80"

total_dismissal_reason= ""

# Send Notification
try:
    results = toast('Active Recall Time ⏱️', 'What does "{0}" translate to in french?'.format(info.word),icon=icon_image,selection=info.options, button="Submit", duration="long")
    user_selection = results["user_input"]["selection"]
except Exception as e:
    # print("Error:",str(e))
    total_dismissal_reason=str(results)

# Handle Errors (<ToastDismissalReason.USER_CANCELED: 0>,), (<ToastDismissalReason.TIMED_OUT: 2>,)
if "USER_CANCELED" in total_dismissal_reason: # Canceled = attempts+=1 (result = 2)
    info.update_corrections_stats(2)
    info.update_timeline_stats(info.word,info.answer,2)

elif "TIMED_OUT" in total_dismissal_reason: # Timeout -> wrong
    info.update_corrections_stats(0)
    info.update_timeline_stats(info.word,info.answer,0)

else:
    user_selection = results["user_input"]["selection"] # gather user input
    
    # Result notifications
    if info.answer == user_selection:
        toast('Active Recall Time: Correct ✅', 'Keep up the good work🫡',icon=icon_correct, button="Dismiss") # send out correct notification
        
        info.update_corrections_stats(1) # update stats
        info.update_timeline_stats(info.word,info.answer,1)
    else:
        solutions =info.options.remove(info.answer)
        toast('Active Recall Time: Wrong ❌', 'Don\'t give up\n\nAnswer: {0}\nYour Choice: {1}'.format(info.answer,user_selection),icon=icon_incorrect, button="Dismiss") # send out incorrect notification

        info.update_corrections_stats(0) # update stats
        info.update_timeline_stats(info.word,info.answer,0)
        # Idea: Show translations for all options
                            
