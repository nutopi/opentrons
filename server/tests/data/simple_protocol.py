from opentrons import containers
from opentrons import instruments

plate = containers.load(
    '96-flat',
    'B2',
    'test-plate'
)

tiprack = containers.load(
    'tiprack-200ul',  # container type from library
    'A1',             # slot on deck
    'test-tiprack'
)

p10 = instruments.Pipette(
    name="p10",
    tip_racks=[tiprack],
    min_volume=1,  # These are variable
    axis="b",
    channels=1
)

p10.set_max_volume(10)
p10.pick_up_tip(tiprack[0])
p10.aspirate(5, plate[0])
p10.dispense(5, plate[11])
