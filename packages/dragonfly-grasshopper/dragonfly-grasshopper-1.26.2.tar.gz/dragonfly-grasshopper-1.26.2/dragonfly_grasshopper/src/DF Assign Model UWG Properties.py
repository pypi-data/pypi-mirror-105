# Dragonfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Dragonfly.
#
# Copyright (c) 2021, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Dragonfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Edit the properties of a Dragonfly Model that affect simulation with to the Urban
Weather Generator (UWG).
-

    Args:
        _model: A Dragonfly Model which is to have its Urban Weather Generator (UWG)
            properties assigned.
        _terrain_: A Terrain object that dictates the properties of the street and
            ground beneath the buildings. If None, a default terrain object will be
            generated by analysing all of the buildings in the Model and drawing
            a bounding rectangle in the XY plane around them.
        _traffic_: A TrafficPararameter object that defines the activity and intensity
            of traffic within the urban street canyons. If None, traffic
            intensity will be approximated using the average building
            story count along with a generic traffic schedule.
        tree_cover_: A number from 0 to 1 that defines the fraction of the exposed
            terrain covered by trees. If None, it will be determined by
            evaluating the horizontal area of all ContextShade geometry
            that has a true is_vegetation property.
        grass_cover_: A number from 0 to 1 that defines the fraction of the exposed
            terrain that is covered by grass or shrubs. If None, no grass will
            be assumed for the urban area.

    Returns:
        report: ...
        model: The input Dragonfly Model with its UWG properties re-assigned based
            on the input.
"""

ghenv.Component.Name = 'DF Assign Model UWG Properties'
ghenv.Component.NickName = 'ModelUWG'
ghenv.Component.Message = '1.2.0'
ghenv.Component.Category = 'Dragonfly'
ghenv.Component.SubCategory = '4 :: AlternativeWeather'
ghenv.Component.AdditionalHelpFromDocStrings = '2'

try:  # import the dragonfly dependencies
    from dragonfly.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import dragonfly:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    # check and duplicate the input
    assert isinstance(_model, Model), \
        'Expected Dragonfly Model. Got {}.'.format(type(_model))
    model = _model.duplicate()

    # assign any of the input properties
    if _terrain_ is not None:
        model.properties.uwg.terrain = _terrain_
    if _traffic_ is not None:
        model.properties.uwg.traffic = _traffic_
    if tree_cover_ is not None:
        model.properties.uwg.tree_coverage_fraction = tree_cover_
    if grass_cover_ is not None:
        model.properties.uwg.grass_coverage_fraction = grass_cover_

    # print some useful information about the model
    print('{} m - average height'.format(
        round(model.average_height_above_ground, 1)))
    print('{} - footprint density'.format(
        round(model.properties.uwg.footprint_density, 2)))
    print('{} - facade to site'.format(
        round(model.properties.uwg.facade_to_site, 2)))
    print('{} - tree cover'.format(
        round(model.properties.uwg.tree_coverage_fraction, 2)))
    print('{} - grass cover'.format(
        round(model.properties.uwg.grass_coverage_fraction, 2)))
