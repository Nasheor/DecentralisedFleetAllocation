from dataclasses import dataclass

@dataclass
class Sec(object):
    sec_id: int
    '''
     - charge_generation varible holds the type of energy generation for the sec
             1: weibull distribution
             2: normal distribution
             3: poisson distribution
    '''
    charge_generation: int
    x_start: int
    y_start: int
    x_end: int
    y_end: int
    charge: int
    total_energy: int

@dataclass
class Ev(object):
    sec_id: int
    battery_capacity: int
    ev_id: int
    num_passengers: int
    charge_per_block: int
    release_time: int

@dataclass
class Passenger(object):
    p_id: int
    sec_id: int


@dataclass
class Trip_petition(object):
    petition_id: int
    passenger_id: int
    time: int
    pickup_x: int
    pickup_y: int
    drop_x: int
    drop_y: int
    early_start: int
    early_finish: int
    late_start: int
    late_finish: int
    travel_time: int