# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------

# ------------------------------------------
# IMPORTS
# ------------------------------------------
import misc
#
import sys
import time
import codecs


# ----------------------------------------------------
# FUNCTION 01 - select_case_based_on_time_window
# ----------------------------------------------------
# Description:
# Given the trip petition and the EV movement, we decide in which case we find ourselves at.
# ----------------------------------------------------
# Input Parameters:
# (1) ta. Integer => Represents the time of the start of the EV movement.
# (2) tb. Integer => Represents the time of the end of the EV movement.
# (3) tp_lb. Integer => Represents the start of the time window where we can consider accommodating the action.
# (4) UB. Integer => Represents the end of the time window where we can consider accommodating the action.
# ----------------------------------------------------
# Output Parameters:
# (1) action_movement_index. Integer. => Case to be considered.
# ----------------------------------------------------
def select_case_based_on_time_window(ta,
                                     tb,
                                     tp_lb,
                                     tp_ub
                                    ):

    # 1. We create the output variable
    res = -1

    # 2. We select the appropriate case
    # CASE -1: The action cannot be accomplished.
    # CASE 0: The action cannot be decided with this movement, let's try straightaway with the next one.
    # CASE > 0: The action might be accommodated with this movement, let's reason with it.

    # 2.1. When the movement starts once the window has finished
    if (ta > tp_ub):
        res = -1

    # 2.2. When the movement starts just when the window is about to finish
    elif (ta == tp_ub):
        res = 1

    # 2.3. When the movement starts before the window is finished and
    #           the movement finishes before the window starts or when it is about to start
    #      elif (ta < tp_ub) and (tb <= tp_lb)
    #      We avoid the first condition as it is clear by not having entered in 2.1 nor in 2.2.
    elif (tb <= tp_lb):
        res = 0

    # 2.4. When the movement starts before the window is finished and
    #           the movement finishes after the window has started
    #      elif (ta < tp_ub) and (tb > tp_lb)
    #      We avoid both conditions as they are clear by not having entered in 2.1 nor in 2.2 nor in 2.3.

    # 2.4.1. CASE 2
    elif ((ta < tp_lb) and (tb < tp_ub)):
        res = 2

    # 2.4.2. CASE 3
    elif ((ta < tp_lb) and (tb == tp_ub)):
        res = 3

    # 2.4.3. CASE 4
    elif ((ta < tp_lb) and (tb > tp_ub)):
        res = 4

    # 2.4.4. CASE 5
    elif ((ta == tp_lb) and (tb < tp_ub)):
        res = 5

    # 2.4.5. CASE 6
    elif ((ta == tp_lb) and (tb == tp_ub)):
        res = 6

    # 2.4.6. CASE 7
    elif ((ta == tp_lb) and (tb > tp_ub)):
        res = 7

    # 2.4.7. CASE 8
    elif ((ta > tp_lb) and (tb < tp_ub)):
        res = 8

    # 2.4.8. CASE 9
    elif ((ta > tp_lb) and (tb == tp_ub)):
        res = 9

    # 2.4.9. CASE 10
    elif ((ta > tp_lb) and (tb > tp_ub)):
        res = 10

    # 3. We return res
    return res


# ----------------------------------------------------
# FUNCTION 02 - compute_distance_among_two_points
# ----------------------------------------------------
# Description:
# Given two points in the city, computes the distance among them.
# ----------------------------------------------------
# Input Parameters:
# (1) SX. Integer. Represents the X-axis of the source location.
# (2) SY. Integer. Represents the Y-axis of the source location.
# (3) TX. Integer. Represents the X-axis of the target location.
# (4) TY. Integer. Represents the Y-axis of the target location.
# ----------------------------------------------------
# Output Parameters:
# (1) res. Integer. => Distance from source to target.
# ----------------------------------------------------
def compute_distance_among_two_points(SX,
                                      SY,
                                      TX,
                                      TY
                                     ):

    # 1. We output the result variable
    res = abs(TX-SX) + abs(TY-SY)

    # 2. We return res
    return res


# ----------------------------------------------------
# FUNCTION 03 - is_extra_energy_and_delay_assumed
# ----------------------------------------------------
# Description:
# Given the remaining schedule after accommodating an action, it computes whether subsequent trips can assume the extra delay or not.
# It also updates each movement with the extra energy consumed.
# ----------------------------------------------------
# Input Parameters:
# (1) my_remaining_EV_schedule. list[Movement]. Represents the remaining schedule of the EV after accommodating the action.
# (2) extra_energy. Integer. Represents the extra energy to be assumed by subsequent trips.
# (3) extra_delay. Integer. Represents the extra delay to be assumed by subsequent trips.
# ----------------------------------------------------
# Output Parameters:
# (1) is_satisfied. Boolean. => True if it is assumed and False otherwise.
# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
# ----------------------------------------------------
def is_extra_energy_and_delay_assumed(my_remaining_EV_schedule,
                                      extra_energy,
                                      extra_delay
                                     ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output if it is_satisfied
    is_satisfied = True

    # 1.2. We output my_remaining_EV_schedule
    pass

    # 2. We traverse the movements
    index = 0
    size = len(my_remaining_EV_schedule)

    while ( (is_satisfied == True) and (index < (size - 1)) ):
        # 2.1. We pick the movement
        (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_remaining_EV_schedule[index]

        # 2.2. We update the energy
        NES = ES - extra_energy
        NEE = EE - extra_energy

        # 2.3. If it was a non-resting movement
        if (TL != 0):
            # 2.3.1. We update its values
            NTA = TA + extra_delay
            NTB = TB + extra_delay
            NLW = LW - extra_delay

            # 2.3.2. If it could not assume the extra delay, we return False
            if (NLW < 0):
                is_satisfied = False
            # 2.3.3. Otherwise, we update the movement
            else:
                new_mov = (NTA, NTB, AX, AY, BX, BY, PS, PE, NES, NEE, TL, NLW, TD)
                my_remaining_EV_schedule[index] = new_mov

        # 2.4. If it was a resting movement
        else:
            # 2.4.1. We delay the start
            NTA = TA + extra_delay

            NTB = None
            NLW = None

            # 2.4.2. If the delay was bigger or equal than the leeway, then we consume the entire resting time
            if (extra_delay >= LW):
                NTB = NTA
                NLW = 0
                extra_delay -= LW

            # 2.4.3. Otherwise, if delay is smaller than the leeway, then we consume just the needed part.
            else:
                NLW = (LW - extra_delay)
                NTB = NTA + NLW
                extra_delay = 0

            # 2.4.4. In any case, we update the movement
            new_mov = (NTA, NTB, AX, AY, BX, BY, PS, PE, NES, NEE, TL, NLW, TD)
            my_remaining_EV_schedule[index] = new_mov

        # 2.5. We check the next movement
        index += 1

    # 3. If we get to the last movement, we process it
    if (is_satisfied == True):
        # 3.1. If we have not accommodated all the extra delay, then it is not feasible
        if (extra_delay > 0):
            is_satisfied = False
        # 3.2. If still feasible, we just update the energy of the last trip
        else:
            if (my_remaining_EV_schedule != []):
                (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_remaining_EV_schedule[index]
                NES = ES - extra_energy
                NEE = EE - extra_energy
                new_mov = (TA, TB, AX, AY, BX, BY, PS, PE, NES, NEE, TL, LW, TD)
                my_remaining_EV_schedule[index] = new_mov

    # 4. We assign res
    res = (is_satisfied, my_remaining_EV_schedule)

    # 5. We return res
    return res


# ------------------------------------------------------------------
# FUNCTION 04 - get_rid_of_redundant_resting_trips
# ------------------------------------------------------------------
# Description:
# Given a valid schedule, to which the action has been accommodated, we update it by removing any redundant resting movement.
# ----------------------------------------------------
# Input Parameters:
# (1) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
# (2) candidate_index. Integer. Represents the movement where the action was attempted to be inserted at.
# (3) res_offset. Integer. Represents the offset with respect to movement_index where the action was finally inserted at.
# ----------------------------------------------------
# Output Parameters:
# (1) res_offset. Integer. => Represents the new offset after all redundant movements are removed.
# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly.
# ----------------------------------------------------
def get_rid_of_redundant_resting_trips(my_EV_schedule,
                                       candidate_index,
                                       res_offset
                                      ):
    # 1. We output the result variable
    res = ()

    # 1.1. We output if it is_satisfied
    pass

    # 1.2. We output my_remaining_EV_schedule
    pass

    # 2. We remove any empty resting movement
    movement_index = len(my_EV_schedule) - 1
    while (movement_index >= 0):
        # 2.1. We get the movement
        (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[movement_index]

        # 2.2. If it is an empty resting movement
        if ((TL == 0) and (TA == TB)):
            # 2.2.1. We remove it
            del my_EV_schedule[movement_index]

            # 2.2.2. If it was a movement prior to where we place the action, we update the offset
            if ( movement_index < (candidate_index + res_offset) ):
                res_offset -= 1

        # 2.3. We decrease movement_index
        movement_index -= 1

    # 3. We remove any consecutive resting movements
    movement_index = len(my_EV_schedule) - 2
    while (movement_index > 0):
        # 3.1. We get the two consecutive movements
        (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[movement_index - 1]
        (NTA, NTB, NAX, NAY, NBX, NBY, NPS, NPE, NES, NEE, NTL, NLW, NTD) = my_EV_schedule[movement_index]

        # 3.2. If they are consecutive resting movements
        if ((TL == 0) and (NTL == 0)):
            # 3.2.1. We remove the second resting movement
            del my_EV_schedule[movement_index]

            # 3.2.2. We update the first resting movement to now combine both
            new_mov = (TA, NTB, AX, AY, NBX, NBY, PS, NPE, ES, NEE, 0, NTB - TA, 0)
            my_EV_schedule[movement_index - 1] = new_mov

            # 3.2.3. If it was a movement prior to where we place the action, we update the offset
            if (movement_index < (candidate_index + res_offset)):
                res_offset -= 1

        # 3.4. We decrease movement_index
        movement_index -= 1

    # 4. We assign res
    res = (res_offset, my_EV_schedule)

    # 5. We return res
    return res


# ------------------------------------------------------------------
# FUNCTION 05 - ev_action_and_movement_allocation_attempt
# ------------------------------------------------------------------
# Description:
# We decide whether the EV can accommodate an action by considering two consecutive movements of its schedule.
# ----------------------------------------------------
# Input Parameters:
# (1) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
# (2) tp_id. Integer. Represents the trip identifier.
# (3) my_TP_static_info. tuple( LB, SX, SY, TX, TY, EP, LP, ED, UB ). Represents the trip info, where:
# (4) max_passengers. Integer. Represents the maximum number of passengers the EV supports.
# (5) movement_index. Integer. Represents the index on the movement we are considering for allocating the action.
# ----------------------------------------------------
# Output Parameters:
# (1) res_offset. Integer. => Represents whether:
#                      - The action cannot be allocated at all (-2)
#                      - The action cannot be allocated in this movement (-1)
#                      - The action can be allocated (>= 0), and the action is entered in the new schedule at position
#                                                            my_EV_schedule[ movement_index + res ]
# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
# ----------------------------------------------------
def ev_action_and_movement_allocation_attempt(my_EV_schedule,
                                              tp_id,
                                              my_TP_static_info,
                                              max_passengers,
                                              movement_index,
                                             ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output the res_offset
    res_offset = 0

    # 1.2. We output my_EV_schedule
    pass

    # 2. We unpack the trip static info
    (LB, SX, SY, TX, TY, EP, LP, ED, LD) = my_TP_static_info

    # 3. We unpack the EV movement we are considering
    (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[movement_index]

    # 4. We unpack the next EV movement to the one we are considering
    (NTA, NTB, NAX, NAY, NBX, NBY, NPS, NPE, NES, NEE, NTL, NLW, NTD) = my_EV_schedule[movement_index + 1]

    # 5. When ensure they are two consecutive movements, and that the first is indeed a resting movement
    assert (TL == 0)
    # NOTE: assert (NTL != 0)
    # assert (AX == BX)
    # assert (AY == BY)
    #assert (PS == PE) => Case 1 leads to resting trips picking-up or dropping-off passengers.
    # assert (ES == EE)
    # assert (LW == (TB-TA))
    # assert (TD == 0)
    # assert (NTA == TB)
    # assert (NAX == BX)
    # assert (NAY == BY)
    # assert (NPS == PE)
    # assert (NES == EE)

    # 6. We compute the distances d1, d2 and d3
    d1 = compute_distance_among_two_points(AX, AY, SX, SY)
    d2 = compute_distance_among_two_points(SX, SY, NBX, NBY)
    d3 = compute_distance_among_two_points(AX, AY, NBX, NBY)
    if (tp_id < 0):
        d1 = compute_distance_among_two_points(AX, AY, TX, TY)
        d2 = compute_distance_among_two_points(TX, TY, NBX, NBY)

    extra_energy = (d1 + d2) - d3
    assert (extra_energy >= 0)

    # 7. We compute the destination of the trip t1.
    t1_x_dest = SX
    t1_y_dest = SY
    if (tp_id < 0):
        t1_x_dest = TX
        t1_y_dest = TY

    # 8. We compute the time-milestones for the two trips 't1' and 't2'

    # 8.1. Trip 't1' early arrival
    t1_ea = EP
    if (tp_id < 0):
        t1_ea = ED

    # 8.2. Trip 't1' late arrival
    t1_la = LP
    if (tp_id < 0):
        t1_la = LD

    # 8.3. Trip 't2' early arrival.
    #      Technically, with the new re-routing to accommodate the action, we could complete 't2' earlier than NTB,
    #      but we do not allow this situation to happen, making an extra rest trip beforehand if needed.
    t2_ea = NTB

    # 8.4. Trip 't2' late arrival
    t2_la = NTB + NLW

    # 8.5. Trip 't1' start time
    start_time = TA
    if ((tp_id > 0) and (TA < LB)):
        start_time = LB

    # 8.6. Trip 't1' arrival time (might be modified later on if it was too early)
    t1_arrival_time = start_time + d1

    # 8.7. Trip 't2' start time
    t2_start_time = t1_arrival_time
    if (t2_start_time < t1_ea):
        t2_start_time = t1_ea

    # 8.8. Trip 't2' arrival time (might be modified later on if it was too early)
    t2_arrival_time = t2_start_time + d2

    # 9. If we cannot make it on time for 't1_la', then we fully discard this action; neither this movement nor any
    #    other further movement will be able to accommodate the action.
    if (t1_arrival_time > t1_la):
        res_offset = -2

    # 10. If we can make it on time for 't1_la' but not for 't2_la', then we discard this action by now and
    #     come back to the main loop of 'ev_action_allocation_attempt' to try with the next movement.
    #     As this means that this movement would have made it on time to pick or drop the passenger, but at the
    #     expense of screwing up an already arranged further movement of the schedule.
    #     We do not allow for this to happen: once one trip (and its associated movements) are approved, they can
    #     not be further revoked.
    if ((res_offset == 0) and (t2_arrival_time > t2_la)):
        res_offset = -1

    # 11. If we are already at the maximum capacity with our passengers, then we cannot accommodate a pick-up action by now and
    #     we come back to the main loop of 'ev_action_allocation_attempt' to try with the next movement.
    if ((res_offset == 0) and (tp_id > 0) and ((NPS == max_passengers) or (NPE == max_passengers)) ):
        res_offset = -1

    # 12. If the energy left in the EV after its very last movement is smaller than the one we need
    #     to accommodate the action with this current movement, then we cannot accommodate the action by now and
    #     we come back to the main loop of 'ev_action_allocation_attempt' to try with the next movement.
    #     Please note we return -1 and not -2 as there might be a further movement where the extra energy needed to
    #     accommodate the action is smaller than the 'extra_energy' required to accommodate it here.
    if ((res_offset == 0) and (extra_energy > my_EV_schedule[-1][9])):
        res_offset = -1

    # 13. If we still can accommodate the action, we keep our reasoning
    if (res_offset == 0):
        # 13.1. We create the list of new trips to be integrated into the EV schedule
        new_movements = []

        # 13.2. MOVEMENT I. If (TA < start_time) we create a first resting movement for such amount of time
        if (TA < start_time):
            new_mov = (TA, start_time, AX, AY, AX, AY, PS, PS, ES, ES, 0, start_time - TA, 0)
            new_movements.append( new_mov )
            res_offset += 1

        # 13.3. MOVEMENT II. If the t1_arrival_time is too soon, we create another extra resting movement for such amount of time
        extra_rest = t1_ea - t1_arrival_time
        if (extra_rest > 0):
            # 13.3.1. We append the extra movement
            new_mov = (start_time, start_time + extra_rest, AX, AY, AX, AY, PS, PS, ES, ES, 0, extra_rest, 0)
            new_movements.append( new_mov )
            res_offset += 1

            # 13.3.2. We update the arrival time
            t1_arrival_time = t1_ea

        # Otherwise, we just make extra_rest = 0
        else:
            extra_rest = 0

        # 13.4. MOVEMENT III. We enter the movement for the action (t1)
        #                     Note: We deliberately do not increase or decrease the number of passengers of the EV,
        #                           as we do this in the separate function 'update_passengers_of_movements'
        new_mov = (start_time + extra_rest, t1_arrival_time, AX, AY, t1_x_dest, t1_y_dest, PS, PS, ES, ES - d1, tp_id, t1_la - t1_arrival_time, d1)
        new_movements.append( new_mov )

        # 13.5. MOVEMENT IV. If the t2_arrival_time was too soon, we create another extra resting movement for such amount of time
        #                     Note: We deliverately do not increase or decrease the number of passengers of the EV,
        #                           as we do this in the separate function 'update_passengers_of_movements'
        extra_rest = t2_ea - t2_arrival_time
        if (extra_rest > 0):
            # 13.5.1. We append the extra movement
            new_mov = (t2_start_time, t2_start_time + extra_rest, t1_x_dest, t1_y_dest, t1_x_dest, t1_y_dest, PS, PS, ES - d1, ES - d1, 0, extra_rest, 0)
            new_movements.append( new_mov )

            # 13.5.2. We update the arrival time
            t2_arrival_time = t2_ea

        # Otherwise, we just make extra_rest = 0
        else:
            extra_rest = 0

        # 13.6. MOVEMENT V. We enter the movement for the action (t2)
        #                     Note: We deliverately do not increase or decrease the number of passengers of the EV,
        #                           as we do this in the separate function 'update_passengers_of_movements'
        new_mov = (t2_start_time + extra_rest, t2_arrival_time, t1_x_dest, t1_y_dest, NBX, NBY, NPS, NPE, ES - d1, ES - (d1 + d2), NTL, t2_la - t2_arrival_time, d2)
        new_movements.append( new_mov )

        # 13.7. We compute the extra energy and extra delay we are propagating
        extra_delay = t2_arrival_time - NTB
        assert (extra_delay >= 0)

        # 13.8. We ensure the extra energy and delay can be assumed by subsequent movements
        (is_assumed, my_remaining_schedule) = is_extra_energy_and_delay_assumed(my_EV_schedule[(movement_index + 2):],
                                                                                extra_energy,
                                                                                extra_delay
                                                                               )

        # 13.9. If it cannot be assumed, we try with the next movement
        if (is_assumed == False):
            res_offset = -1
        # 13.10. Otherwise, the action is accommodated
        else:
            # 13.10.1. We put together the final schedule
            my_EV_schedule = my_EV_schedule[:movement_index] + new_movements + my_remaining_schedule

            # 13.10.2. We get rid of empty resting movements and consecutive resting movements
            (res_offset, my_EV_schedule) = get_rid_of_redundant_resting_trips(my_EV_schedule,
                                                                              movement_index,
                                                                              res_offset
                                                                             )

    # 14. We assign res
    res = (res_offset, my_EV_schedule)

    # 15. We return res
    return res


# ----------------------------------------------------
# FUNCTION 06 - last_call_case
# ----------------------------------------------------
# Description:
# Given a concrete movement of the schedule of an EV and an action of the new trip petition (pick-up or drop-off), we decide whether the EV can accommodate such action with this movement.
# ----------------------------------------------------
# Input Parameters:
# (1) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
# (2) tp_id. Integer. Represents the trip identifier.
# (3) my_TP_static_info. tuple( LB, SX, SY, TX, TY, EP, LP, ED, UB ). Represents the trip info.
# (4) max_passengers. Integer. Represents the maximum number of passengers the EV supports.
# (5) movement_index. Integer. Represents the index on the movement we are considering for allocating the action.
# ----------------------------------------------------
# Output Parameters:
# (1) res_offset. Integer. => Represents whether:
#                      - The action cannot be allocated at all (-2)
#                      - The action cannot be allocated in this movement (-1)
#                      - The action can be allocated (>= 0), and the action is entered in the new schedule at position
#                                                            my_EV_schedule[ movement_index + res ]
# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
#                                     Even if it is not explicitly outputted, it is done by modifying the input parameter.
# ----------------------------------------------------
def last_call_case(my_EV_schedule,
                   tp_id,
                   my_TP_static_info,
                   max_passengers,
                   movement_index,
                  ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output the res_offset
    res_offset = -2

    # 1.2. We output my_EV_schedule
    pass

    # 2. We unpack the trip static info
    (LB, SX, SY, TX, TY, EP, LP, ED, LD) = my_TP_static_info

    # 3. We unpack the EV movement we are considering
    (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[movement_index]

    # 4. If it was a pick-up action the EV was at the exact same location when it started the movement,
    #    then we assume we are still on time to pick-up the passenger
    if ((tp_id > 0) and (AX == SX) and (AY == SY) and (PS < max_passengers)):
        # 4.1. We allocate the action
        res_offset = 0

        # 4.2. We create the new movement
        new_movement = (TA, TA, SX, SY, SX, SY, PS, PS + 1, ES, ES, tp_id, 0, 0)

        # 4.3. We update the schedule by inserting the new movement to it
        my_EV_schedule.insert(movement_index, new_movement)

    # 5. Alternatively, if it was a drop-off action the EV was at the exact same location when it started the movement,
    #    then we assume we are still on time to pick-up the passenger
    if ((tp_id < 0) and (AX == TX) and (AY == TY)):
        # 5.1. We allocate the action
        res_offset = 0

        # 5.2. We create the new movement
        new_movement = (TA, TA, TX, TY, TX, TY, PS, PS - 1, ES, ES, tp_id, 0, 0)

        # 5.3. We update the schedule by inserting the new movement to it
        my_EV_schedule.insert(movement_index, new_movement)

    # 6. We assign res
    res = (res_offset, my_EV_schedule)

    # 7. We return res
    return res


# ----------------------------------------------------
# FUNCTION 07 - normal_call_case
# ----------------------------------------------------
# Description:
# Given a concrete movement of the schedule of an EV and an action of the new trip petition (pick-up or drop-off), we decide whether the EV can accommodate such action with this movement.
# ----------------------------------------------------
# Input Parameters:
# (1) case_number. Integer. The case this movement represents with respect to the trip petition.
# (2) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
# (3) tp_id. Integer. Represents the trip identifier.
# (4) my_TP_static_info. tuple( LB, SX, SY, TX, TY, EP, LP, ED, UB ). Represents the trip info.
# (5) max_passengers. Integer. Represents the maximum number of passengers the EV supports.
# (6) movement_index. Integer. Represents the index on the movement we are considering for allocating the action.
# ----------------------------------------------------
# Output Parameters:
# (1) res_offset. Integer. => Represents whether:
#                      - The action cannot be allocated at all (-2)
#                      - The action cannot be allocated in this movement (-1)
#                      - The action can be allocated (>= 0), and the action is entered in the new schedule at position
#                                                            my_EV_schedule[ movement_index + res ]
# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
# ----------------------------------------------------
def normal_call_case(case_number,
                     my_EV_schedule,
                     tp_id,
                     my_TP_static_info,
                     max_passengers,
                     movement_index,
                    ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output the res_offset
    res_offset = -1

    # 1.2. We output my_EV_schedule
    pass

    # 2. We unpack the trip static info
    (LB, SX, SY, TX, TY, EP, LP, ED, LD) = my_TP_static_info

    # 3. We unpack the EV movement we are considering
    (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[movement_index]

    # 4. If the movement is resting
    if (TL == 0):
        (res_offset, my_EV_schedule) = ev_action_and_movement_allocation_attempt(my_EV_schedule,
                                                                                 tp_id,
                                                                                 my_TP_static_info,
                                                                                 max_passengers,
                                                                                 movement_index,
                                                                                )

    # 5. If the movement is not resting
    else:
        # 5.1. For cases 2, 3 and 4 we can directly discard the trip.
        #      For cases 5 to 10, we need to insert a fake resting trip and do the same logic afterwards
        if (case_number > 4):
            # 5.1.1. We insert the fake resting trip
            new_mov = (TA, TA, AX, AY, AX, AY, PS, PS, ES, ES, 0, 0, 0)
            my_EV_schedule.insert( movement_index, new_mov )

            # 5.1.2. We apply the logic afterwards
            (res_offset, my_EV_schedule) = ev_action_and_movement_allocation_attempt(my_EV_schedule,
                                                                                     tp_id,
                                                                                     my_TP_static_info,
                                                                                     max_passengers,
                                                                                     movement_index,
                                                                                    )

    # 6. We assign res
    res = (res_offset, my_EV_schedule)

    # 7. We return res
    return res


# ----------------------------------------------------------------
# FUNCTION 08 - update_passengers_of_movements
# ----------------------------------------------------------------
# Description:
# Given a trip attempted by picking-up and dropping-off the passenger at concrete movements,
# we ensure the EV had enough space for this extra passenger during the time she was on it.
# ----------------------------------------------------
# Input Parameters:
# (1) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
# (2) pick_up_movement_index. Integer. Represents the index on the movement we are considering for allocating the pick-up action.
# (3) drop_off_movement_index. Integer. Represents the index on the movement we are considering for allocating the drop-off action.
# (4) max_passengers. Integer. Represents the maximum number of passengers the EV supports.
# ----------------------------------------------------
# Output Parameters:
# (1) is_satisfied. Boolean. => Represents whether there was enough space in the EV.
# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly the number of passengers
#                                     between the pick-up and the drop-off.
# ----------------------------------------------------
def update_passengers_of_movements(my_EV_schedule,
                                   pick_up_movement_index,
                                   drop_off_movement_index,
                                   max_passengers
                                  ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output the res_offset
    is_satisfied = True

    # 1.2. We output my_EV_schedule
    pass

    # 2. We update the pick_up_movement_index by increasing its number of passengers
    (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[pick_up_movement_index]
    NPE = PE + 1
    if (NPE > max_passengers):
        is_satisfied = False
    else:
        # 2.4.1. We update the schedule
        new_movement = (TA, TB, AX, AY, BX, BY, PS, NPE, ES, EE, TL, LW, TD)
        my_EV_schedule[pick_up_movement_index] = new_movement

    # 3. We traverse all indexes from pick-up (not included) until drop-off (included), adding the passenger to all of them
    movement_index = pick_up_movement_index + 1

    while ((is_satisfied == True) and (movement_index < drop_off_movement_index)):
        # 3.1. We take the schedule movement
        (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[movement_index]

        # 3.2. We update the passengers
        NPS = PS + 1
        NPE = PE + 1

        # 3.3. If the new number of passengers is not valid, we discard the trip petition
        if ((NPS > max_passengers) or (NPE > max_passengers)):
            is_satisfied = False

        # 3.4. Otherwise
        else:
            # 3.4.1. We update the schedule
            new_movement = (TA, TB, AX, AY, BX, BY, NPS, NPE, ES, EE, TL, LW, TD)
            my_EV_schedule[movement_index] = new_movement

            # 3.4.2. We continue with the next index
            movement_index += 1

    # 4. We update the drop_off_movement_index by decreasing its number of passengers
    (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[drop_off_movement_index]
    NPS = PS + 1
    if (NPS > max_passengers):
        is_satisfied = False
    else:
        # 2.4.1. We update the schedule
        new_movement = (TA, TB, AX, AY, BX, BY, NPS, PE, ES, EE, TL, LW, TD)
        my_EV_schedule[drop_off_movement_index] = new_movement

    # 5. We assign res
    res = (is_satisfied, my_EV_schedule)

    # 6. We return res
    return res


# ----------------------------------------------------
# FUNCTION 09 - ev_action_allocation_attempt
# ----------------------------------------------------
# Description:
# Given the schedule of an EV and an action of the new trip petition (pick-up or drop-off), we decide whether the EV can accommodate such action.
# ----------------------------------------------------
# Input Parameters:
# (1) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
# (2) tp_id. Integer. Represents the trip identifier.
# (3) my_TP_static_info. tuple( LB, SX, SY, TX, TY, EP, LP, ED, UB ). Represents the trip info, where:
# (4) max_passengers. Integer. Represents the maximum number of passengers the EV supports.
# (5) start_index. Integer. Represents the index on the movement list that we start considering for allocating the action.
# ----------------------------------------------------
# Output Parameters:
# (1) res_index. Integer. => Index in the schedule of the movement where the action has been accommodated.
#                                         -1 if not accommodated.

# (2) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
# ----------------------------------------------------
def ev_action_allocation_attempt(my_EV_schedule,
                                 tp_id,
                                 my_TP_static_info,
                                 max_passengers,
                                 start_index,
                                ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output the res_index
    res_index = -1

    # 1.2. We output my_EV_schedule
    pass

    # 2. We unpack the trip static info
    (LB, SX, SY, TX, TY, EP, LP, ED, LD) = my_TP_static_info

    # 3. We evaluate the trip action lower and upper bound

    # 3.1. If it is a pick-up action, then the window is
    #        from when the trip is announced
    #        until the late pick-up
    if (tp_id > 0):
        tp_lb = LB
        tp_ub = LP

    # 3.2. If it is a drop-off action, then the window is
    #        from the start time of the movement after the pick-up
    #        until the late drop-off
    else:
        tp_lb = my_EV_schedule[start_index][0]
        tp_ub = LD

    # 4. We traverse the different movements of the schedule
    #    while we still have not accommodated the action and there are more candidate movements to try

    #    NOTE: we now traverse until the second very last movement as, on EV creation, we are now incorporating it with
    #          a very last resting trip, at the SEC, of size 1, but with leeway 0, so that it cannot be moved.
    #          In other words, we force all the EVs to be back in the SEC before the last time step of the simulation.
    size = len(my_EV_schedule) - 1
    movement_index = start_index

    while ((res_index == -1) and (movement_index < size)):
        # 4.1. We get the start and end times for the EV movement
        ta = my_EV_schedule[movement_index][0]
        tb = my_EV_schedule[movement_index][1]

        # 4.2. We distinguish the concrete case we are dealing with:
        case = select_case_based_on_time_window(ta,
                                                tb,
                                                tp_lb,
                                                tp_ub
                                               )

        # 4.3. If the action cannot be accomplished, we discard it altogether
        if (case == -1):
            movement_index = size

        # 4.4. If the action cannot be decided with this movement, let's try straightaway with the next one
        elif (case == 0):
            movement_index += 1

        # 4.5. If the action might be accommodated with this movement, let's reason with it
        elif (case > 0):
            # 4.5.1. We make a copy of the schedule, to play with it
            my_new_EV_schedule = my_EV_schedule[:]

            # 4.5.2. If we are in a last call case, we process it
            res_offset = None
            if (case == 1):
                (res_offset, my_new_EV_schedule) = last_call_case(my_new_EV_schedule,
                                                                  tp_id,
                                                                  my_TP_static_info,
                                                                  max_passengers,
                                                                  movement_index
                                                                 )

            # 4.5.3. If we are not in a last call case, we process it as well
            else:
                (res_offset, my_new_EV_schedule) = normal_call_case(case,
                                                                    my_new_EV_schedule,
                                                                    tp_id,
                                                                    my_TP_static_info,
                                                                    max_passengers,
                                                                    movement_index
                                                                   )

            # 4.5.4. If we succeeded, we stop the loop and update the schedule
            if (res_offset >= 0):
                res_index = movement_index + res_offset
                my_EV_schedule = my_new_EV_schedule

            # 4.5.5. Otherwise, we keep trying with the next candidate
            else:
                movement_index += 1

    # 6. We assign res
    res = (res_index, my_EV_schedule)

    # 7. We return res
    return res


# ----------------------------------------------------
# FUNCTION 10 - ev_return_to_sec_allocation_attempt
# ----------------------------------------------------
# Description:
# Given the schedule of an EV and a new trip petition, we check if the EV comes back to the SEC. Otherwise, we try to accommodate such trip as well.
# ----------------------------------------------------
# Input Parameters:

# (1) my_EV_schedule. [( TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD )]. => The schedule of the EV, as the list of Movements. Each movement is represented as a tuple, where:
# (2) sec_x_location. The X-axis of the SEC, in case the EV has to come back to it.
# (3) sec_y_location. The Y-axis of the SEC, in case the EV has to come back to it.
# ----------------------------------------------------
# Output Parameters:
# (1) res_index. Integer. => Index in the schedule of the movement to come back to the SEC.
#                                               -1 if not possible to come back.

# (2) my_EV_schedule. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
# ----------------------------------------------------
def ev_return_to_sec_allocation_attempt(my_EV_schedule,
                                        sec_x_location,
                                        sec_y_location
                                       ):

    # 1. We output the result variable
    res = ()

    # 1.1. We output the res_index
    res_index = -1

    # 1.2. We output my_EV_schedule
    pass

    # 2. We get the index of the second last movement
    candidate_index = len(my_EV_schedule) - 1

    # 3. We unpack the candidate index from the EV schedule
    (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD) = my_EV_schedule[candidate_index]

    # 4. If the EV was already coming back to the SEC, then all is good
    if ((BX == sec_x_location) and (BY == sec_y_location)):
        res_index = candidate_index
        if (TL != 1000000000):
            my_EV_schedule[candidate_index] = (TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, 1000000000, LW, TD)

    # 5. We assign res
    res = (res_index, my_EV_schedule)

    # 6. We return res
    return res


# ----------------------------------------------------
# FUNCTION 11 - ev_trip_allocation_attempt
# ----------------------------------------------------
# Description:
# Given the schedule of an EV and a new trip petition, we decide whether the EV can accommodate the trip.
# ----------------------------------------------------
# Input Parameters:

# (1) my_EV_schedule. list[Movement]. Represents the schedule of the EV.
#        Each Movement is a tuple( TA, TB, AX, AY, BX, BY, PS, PE, ES, EE, TL, LW, TD ), where:
#           (00) TA. Integer => Time of the start of the movement.
#           (01) TB. Integer => Time of the end of the movement.
#           (02) AX. Integer => X-axis of the position at the start of the movement.
#           (03) AY. Integer => Y-axis of the position at the start of the movement.
#           (04) BX. Integer => X-axis of the position at the end of the movement.
#           (05) BY. Integer => Y-axis of the position at the end of the movement.
#           (06) PS. Integer => Number of passengers at the start of the movement.
#           (07) PE. Integer => Number of passengers at the end of the movement.
#           (08) ES. Integer => Battery left at the start of the movement.
#           (09) EE. Integer => Battery left at the end of the movement.
#           (10) TL. Integer => Movement label.
#           (11) LW. Integer => Leeway or time the movement can be delayed.
#           (12) TD. Integer => Movement distance covered.

# (2) tp_id. Integer. Represents the trip identifier.

# (3) my_TP_static_info. tuple( LB, SX, SY, TX, TY, EP, LP, ED, UB ). Represents the trip info, where:
#           (00) LB. Integer => Time the trip petition is launched / announced.
#           (01) SX. Integer => X-axis of the pick-up position.
#           (02) SY. Integer => Y-axis of the pick-up position.
#           (03) TX. Integer => X-axis of the drop-off position.
#           (04) TY. Integer => Y-axis of the drop-up position.
#           (05) EP. Integer => Time of the early pick-up of the trip petition.
#           (06) LP. Integer => Time of the late pick-up of the trip petition.
#           (07) ED. Integer => Time of the early drop-off of the trip petition.
#           (08) UB. Integer => Time of the late drop-off of the trip petition.

# (4) max_passengers. Integer. Represents the maximum number of passengers the EV supports.
# (5) sec_x_location. Integer. Represents the X-axis of the SEC, in case the EV has to come back to it.
# (6) sec_y_location. Integer. Represents the Y-axis of the SEC, in case the EV has to come back to it.

# ----------------------------------------------------
# Output Parameters:
# (1) is_allocated. Boolean. Represents whether the trip can be allocated or not.
# (2) pick_up_movement_index. Integer. Represents the index in the schedule of the movement to pick-up the passenger.
# (3) is_allocated. Integer. Represents the index in the schedule of the movement to drop-off the passenger.
# (4) is_allocated. Integer. Represents the index in the schedule of the movement to return back to the SEC.
# (5) my_EV_schedule. list[Movement]. Represents the new schedule of the EV, updated accordingly if the trip is allocated.
# ----------------------------------------------------
def ev_trip_allocation_attempt(my_EV_schedule,
                               tp_id,
                               my_TP_static_info,
                               max_passengers,
                               sec_x_location,
                               sec_y_location
                              ):
    # 1. We output the result variable
    res = ()

    # 1.1. We output whether the attempt was successful
    is_allocated = False

    # 1.2. We ouptut the pick-up movement index
    pick_up_movement_index = -1

    # 1.3. We ouptut the drop-off movement index
    drop_off_movement_index = -1

    # 1.4. We ouptut the drop-off movement index
    return_to_sec_movement_index = -1

    # 1.5. We output the extra conditions
    extra_passenger_energy_and_delay_constraints_satisfied = False

    # 1.6. We output my_EV_schedule
    pass

    # 2. We make a copy of the schedule to play with it
    new_EV_schedule = my_EV_schedule[:]

    # 2. We attempt to pick-up the passenger
    (pick_up_movement_index, new_EV_schedule) = ev_action_allocation_attempt(new_EV_schedule,
                                                                             tp_id,
                                                                             my_TP_static_info,
                                                                             max_passengers,
                                                                             0
                                                                            )

    # 3. If pick-up succeeded, we attempt to drop-off the passenger
    if (pick_up_movement_index >= 0):
        (drop_off_movement_index, new_EV_schedule) = ev_action_allocation_attempt(new_EV_schedule,
                                                                                  (-1) * tp_id,
                                                                                  my_TP_static_info,
                                                                                  max_passengers,
                                                                                  pick_up_movement_index + 1
                                                                                 )

    # 4. If drop-off succeeded, we ensure that the new_EV_schedule ends up back on the SEC
    if (drop_off_movement_index >= 0):
        (return_to_sec_movement_index, new_EV_schedule) = ev_return_to_sec_allocation_attempt(new_EV_schedule,
                                                                                              sec_x_location,
                                                                                              sec_y_location
                                                                                             )

    # 5. If pick-up, drop-off and return to SEC succeeded, we ensure the extra passengers, energy and delay constraints
    if (return_to_sec_movement_index >= 0):
        (extra_passenger_energy_and_delay_constraints_satisfied, new_EV_schedule) = \
            update_passengers_of_movements(new_EV_schedule,
                                           pick_up_movement_index,
                                           drop_off_movement_index,
                                           max_passengers
                                          )

    # 7. If the trip is allocated, we update my_EV_schedule
    if ( (pick_up_movement_index >= 0) and
         (drop_off_movement_index >= 0) and
         (return_to_sec_movement_index >= 0) and
         (extra_passenger_energy_and_delay_constraints_satisfied == True)
       ):

        # 7.1. We mark the trip petition as allocated to the EV
        is_allocated = True

        # 7.2. We get its final schedule
        my_EV_schedule = new_EV_schedule

    # 7. We assign res
    res = (is_allocated,
           pick_up_movement_index,
           drop_off_movement_index,
           return_to_sec_movement_index,
           extra_passenger_energy_and_delay_constraints_satisfied,
           my_EV_schedule
          )

    # 8. We return res
    return res


# ------------------------------------------
# FUNCTION 12 - solve_reactive_simulation
# ------------------------------------------
def solve_reactive_simulation(SECs,
                              EVs,
                              TPs
                             ):

    # 1. We create the output variable
    res = 0

    # 2. We get the ids of the TPs and EVs
    TP_IDs = sorted(TPs.keys())
    EV_IDs = sorted(EVs.keys())

    # 3. We traverse each trip, in order to allocate it
    for tp_id in TP_IDs:
        # 3.1. We traverse each vehicle, to try to allocate the trip to it
        for ev_id in EV_IDs:
            # 3.1.1. We setup the algorithm
            (my_EV_static_info, my_EV_schedule) = EVs[ev_id]
            max_passengers = my_EV_static_info[3]
            (my_TP_static_info, my_TP_SEC, my_TP_EV) = TPs[tp_id]
            (sec_x_location, sec_y_location) = SECs[my_EV_static_info[0]]

            # 3.1.2. We run the algorithm
            (is_allocated,
             pick_up_movement_index,
             drop_off_movement_index,
             return_to_sec_movement_index,
             extra_passenger_energy_and_delay_constraints_satisfied,
             my_new_EV_schedule
             ) = ev_trip_allocation_attempt(my_EV_schedule,
                                            tp_id,
                                            my_TP_static_info,
                                            max_passengers,
                                            sec_x_location,
                                            sec_y_location
                                           )

            # 3.1.3. If the vehicle was allocated
            if (is_allocated == True):
                # I. We update the schedule of the EV
                EVs[ev_id][1] = my_new_EV_schedule

                # II. We update the info of TP_allocation
                TPs[tp_id][2] = ev_id

                # III. We increase the number of petitions satisfied
                res += 1

                # IV. We do not try to allocate it to any other EVs
                break

    # 4. We return res
    return res


# ------------------------------------------
# FUNCTION 13 - solve_instance
# ------------------------------------------
def solve_instance(input_file_name, output_file_name):
    # 1. We create the output variable
    res = 0

    # 2. We parse the instance in
    (city, SECs, EVs, TPs, TDs) = misc.parse_in_subproblem_instance(input_file_name)

    #

    # 3. We run the reactive simulation
    res = solve_reactive_simulation(SECs,
                                    EVs,
                                    TPs
                                   )

    # 4. We parse the instance out
    total_energy = misc.parse_out_subproblem_instance(output_file_name,
                                       res,
                                       EVs,
                                       TPs,
                                       TDs
                                      )

    # 5. We return res
    return res, total_energy


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now its time to apply this knowledge.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer finally processes this PYTHON PROGRAM EXECUTION section, which:
# (i) Specifies the function F to be executed.
# (ii) Define any input parameter such this function F has to be called with.
#
# --------------------------------------------------------
if __name__ == '__main__':
    # 1. We get the name of the input and output folder
    # input_file = "../../2_Instances/b_should_be_easy.txt"
    # output_file = "../../4_Solutions/b_should_be_easy.txt"

    input_file = "./b_should_be_easy.in"
    output_file = "./b_should_be_easy.out"

    if (len(sys.argv) > 1):
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    # 2. We call to the function my_main
    start_time = time.time()

    solve_instance(input_file, output_file)

    total_time = time.time() - start_time
    print("Total time = " + str(total_time))
