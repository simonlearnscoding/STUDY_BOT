

        
# TODO: test
# member = await User.object.get_or_create_user(member) # fetch the user from DB

class decision_tree():
    print('called decision tree')
    def check_which_vc_event_to_trigger(self, before, after, member):
        if self.excluding_condition_is_met(before, after, member):
            return
        if cnd.user_joins_tracking_channel(before, after):
            print('user joins tracking channel ')
            return

        if cnd.user_changed_type_of_tracking(before, after):
            print('user changed tpye of tracking ')
            return

        if cnd.userLeftChannel(after):
            print('user left channel')
            return

        if cnd.userChangedChannel(before, after):
            print('user changed channel')
            
    def excluding_condition_is_met(self, before, after, member):
        print('excluding condition is met')
        if cnd.is_mute_or_deafen_update(before, after):
            return True
        if member.bot:
            return True
        return False
        pass


