#!/usr/bin/env python

"""Unit conversion calculators.

CHANGELOG:
  2005/07/14 CB: Initial import.
  2005/07/15 MO: Latitude and Longitude classes.
  2005/07/18 MO: Limit Latitude range to 90.
  2007/05/03 CB: Tweaked lat-long to get correct answer for 40 minutes.
                 Added "convert" as alias for "Convert"
  2007/12/17 MO: Add .format() method to Latitude/Longitude returning Unicode.
                 .factor_html() remains for backward compatibility, using
                 .format() internally.
                 Make Latitude/Longitude.__repr__ more robust in case
                 .__init__ raises an exception; workaround for Pylons bug
                 http://pylonshq.com/project/pylonshq/ticket/341
  2008/02/22 CB: Added a few more units for Ian
  2008/06/05 CB: Various changes before putting the Converter GUI on the web: new units, changed, spelling, etc.
  2009/09/29 CB: Re-factored the lat-long stuff:
                 - it's not in a separate module
                 - Mike and Chris' code has been merged for less duplication
                 - Unit data moved to separate module
  2014/10/14 CB: MAjor re-factor to make it work with PythonJS.
"""

__version__ = "1.3.0"


## Keeping it all in one file.
ConvertDataUnits = {
# All lengths in terms of meter
# All conversion factors from "Handbook of Chemistry and Physics" (HCP) except where noted.
    
"Length" : {"meter"      : (1.0,["m","meters","metre"]),
            "centimeter" : (0.01,["cm", "centimeters"]),
            "millimeter"  : (0.001,["mm","millimeters"]),
            "micron"  : (0.000001,["microns"]),
            "kilometer"  : (1000.0,["km","kilometers"]),
            "foot"        : (0.3048,["ft", "feet"]),
            "inch"      : (0.0254,["in","inches"]),
            "yard"       : (0.9144,[ "yrd","yards"]),
            "mile"       : (1609.344,["mi", "miles"]),
            "nautical mile" : (1852.0,["nm","nauticalmiles"]),
            "fathom"  : (1.8288,["fthm", "fathoms"]),
            "latitude degree": (111120.0,["latitudedegrees"]),
            "latitude minute": (1852.0,["latitudeminutes"])
            },

# this is technically length but used differently, so I'm keeping it separate
# micron is the base unit
"Oil Concentration" : {"micron"         : (1.0, ["microns"]),
                       "cubic meter per square kilometer" : (1.0,["m^3/km^2",]),
                       "millimeter"     : (1000.,["mm","millimeters"]),
                       "inch"           : (25400.,["in","inches"]),
                       "barrel per acre": (39.2866176,["bbl/acre",]), # calculated from HCP
                       "barrel per square mile": (0.06138533995, ["bbl/sq.mile",]), # calculated from HCP
                       "gallon per acre": (0.93539563202687404,["gal/acre",]), # calculated from HCP
                       "liter per hectare": (0.1,["liter/hectare",]), # calculated from HCP
                       },

# All Areas in terms of square meter
"Area" : {"square meter"  : (1.0,["m^2","sq m"]),
          "square centimeter": (.0001,["cm^2","sq cm"]),
          "square kilometer"  : (1e6,["km^2","sq km"]),
          "acre"  : (4046.8564,["acres"]),
          "square mile"  : (2589988.1,["sq miles"]),
          "square nautical mile"  : (3429904,["sq nm","nm^2"]), # calculated from HCP
          "square yard"  : (0.83612736,["sq yards","squareyards"]),
          "square foot"  : (0.09290304,["ft^2", "sq foot","square feet"]),
          "square inch"  : (0.00064516,["in^2", "sq inch","square inches"]),
          "hectare"  : (10000.0,["hectares","ha"]),
          },

# All volumes in terms of cubic meter
"Volume" : {"cubic meter"  : (1.0,["m^3","cu m","cubic meters"]),
            "cubic kilometer"  : (1e9,["km^3","cu km","cubic kilometers"]),
            "cubic centimeter"  : (1e-6,["cm^3","cu cm", "cc"]),
            "barrel (petroleum)" : (.1589873,["bbl","barrels","barrel","bbls",]),
            "liter"        : (1e-3,["l","liters"]),
            "gallon"       : (0.0037854118, ["gal","gallons","usgal"]),
            "gallon (UK)"  : (0.004546090, ["ukgal","gallons(uk)"]),
            "million US gallon"  : (3785.4118, ["milliongallons","milgal"]),
            "cubic foot"    : (0.028316847, ["ft^3","cu feet","cubicfeet"]),
            "cubic inch"    : (16.387064e-6, ["in^3","cu inch","cubicinches"]),
            "cubic yard"    : (.76455486, ["yd^3","cu yard","cubicyards"]),
            "fluid ounce"      : (2.9573530e-5, ["oz","ounces(fluid)", "fluid oz"]),
            "fluid ounce (UK)" : (2.841306e-5, ["ukoz", "fluid oz(uk)"]),
            },

# All Temperature units in K (multiply by, add)
"Temperature" : {"Kelvin"  : ((1.0, 0.0),["K","degrees k","degree k","degrees kelvin","degree kelvin","deg k"]),
                 "Celsius"  : ((1.0, 273.16),["C","degrees c","degrees celsius","deg c","centigrade"]),
                 "Fahrenheit"  : ((0.55555555555555558, (273.16*(9. / 5.) - 32.0) ),["F","degrees f","degree f","degrees fahrenheit","deg f"]),
                 },

# All Mass units in Kg (weight is taken to be mass at standard g)
"Mass" : {"kilogram"  : (1.0,["kg","kilograms"]),
          "pound"     : (0.45359237,["lb","pounds","lbs"]),
          "gram"  : (.001,["g","grams"]),
          "ton"   : (907.18474, ["tons","uston"]),
          "metric ton (tonne)" : (1000.0, ["tonnes","metric ton","metric tons"]),
          "slug"       : (14.5939, ["slugs"]),
          "ounce"       : (.028349523, ["oz","ounces"]),
          "ton (UK)"       : (1016.0469, ["ukton","long ton"]),
          },

# All Time In second
"Time" : {"second"  : (1.0,["s", "sec","seconds"]),
          "minute"  : (60.0,["min","minutes"]),
          "hour"    : (3600.0,["hr","hours","hrs"]),
          "day"     : (86400.0,["days"]),
          },
# All Velocities in meter per second
"Velocity" : {"meter per second"  : (1.0,["m/s","meters per second","mps"]),
              "meter per minute" : (0.01666666666, ["m/min", "meters per minute"]),
              "centimeter per second"  : (.01,["cm/s"]),
              "kilometer per hour"  : (0.277777,["km/h", "km/hr"]),
              "knot"  : (0.514444,["kts", "knots"]),
              "mile per hour"  : (0.44704,["mph","miles per hour"]),
              "foot per second"  : (0.3048,["ft/s", "ft/sec", "feet per second", "feet/s"]),
              "foot per minute"  : (0.00508,["ft/min", "feet per minute", "feet/min"]),
              "foot per hour"  : (0.000084666, ["ft/hr", "feet per hour", "feet/hour"]),
              },
# All Discharges in cubic meter per second
"Discharge" : {"cubic meter per second"  : (1.0, ["m^3/s","cu m/s","cms"]),
               "cubic meter per min"  : (1.0/60., ["m^3/min",]),
               "cubic meter per hour"  : (1.0/3600.0, ["m^3/hr",]),
               "liter per second"    : (0.001, ["l/s","lps"]),
               "liter per minute"    : (0.001/60, ["l/min",]),
               "cubic foot per second"  : (.02831685, ["cfs","cu feet/s","feet^3/s"]),
               "cubic foot per minute"  : (0.00047194744, ["ft^3/min"]),# calculated from cm^3/s
               "gallon per day"  : (4.3812636805555563e-08, ["gal/day"]),# calculated from gal/hr
               "gallon per hour"  : (1.0515032833333335e-06, ["gal/hr"]),
               "gallon per minute" : (6.3090197000000006e-05, ["gal/min", "gpm"]),
               "gallon per second"  : ( 0.0037854118, ["gal/s", "gal/sec"]),
               "barrel per hour"  : ( 4.4163138888888885e-05, ["bbl/hr"]),
               "barrel per day"  : ( 1.84013078e-06, ["bbl/day"]), # calculated from bbl/hr
               },

### Kinematic Viscosity in Stokes
##  NOTE: there is a more detailed way to do this, specified in:
##        ASTM D 2161 Standard Practice for Conversion of Kinematic
##        Viscosity to Saybolt Universal Viscosity or to Saybolt Furol
##        Viscosity
## for the moment, this will only handle approximation for SFS and SUS
"Kinematic Viscosity" : {"Stoke": (1.0, ["St","stokes"]),
                         "centiStoke": (.01, ["cSt","centistokes"]),
                         "square millimeter per second": (.01, ["mm^2/s",]),
                         "square centimeter per second": (1.0, ["cm^2/s",]),
                         "square meter per second": (10000, ["m^2/s"],),
                         "square inch per second": (6.4516, ["in^2/s","squareinchespersecond"]),
                         "Saybolt Universal Second": (1/462.0, ["SSU","SUS"]),# from CRC - only good for > 100cSt
                         "Saybolt Furol Second": (0.02116959064, ["SSF","SFS"]),# from Fuel Oil Manual: good for 724cSt
                         #"poise" : (["P"])
                         },

### Density in g/cc
## NOTE: Specific Gravity can only be defined for a given reference temperature.
##       The most common standard in the oil industry is 15C (or 60F). The
##       following is the value for the Density of water at 15C
##       (CRC Handbook of Chemistry and Physics) 
"Density" : {"gram per cubic centimeter"  : (1.0,["g/cm^3","grams per cubic centimeter"]),
             u"specific gravity (15\xb0C)"  : (0.99913,["S","specificgravity","Spec grav","SG","specificgravity(15C)"]),
             "kilogram per cubic meter" : (.001,["kg/m^3"]),
             "pound per cubic foot":  (0.016018463,["lbs/ft^3"]),
             "API degree"  : (1,["api"]),# this is special cased in the code.
             },

### Concentration in water in PPM
"Concentration In Water" : {"part per million"  : (1.0,["ppm","parts per million"]),
                            "part per billion"  : (.001,["ppb", "parts per billion"]),
                            "part per thousand" : (1000,["ppt", "parts per thousand"]),
                            "part per trillion" : (.000001,["parts per trillion","pptr"]),
                            "fraction (decimal)" : (1e6,["fraction", "mass per mass"]),
                            "percent"  : (1e4,["%", "parts per hundred", "per cent"]),
                            "kilogram per cubic meter":  (1000,["kg/m^3","kg/m3"]),
                            "pound per cubic foot": (16018.463, ["lb/ft^3"]),
                            "milligram per liter": (1.0, ["mg/l"]),
                            "milligram per kilogram": (1.0, ["mg/kg"]),
                            "milligram per milliliter": (1000, ["mg/ml"]),
                            "microgram per liter": (0.001, ["ug/l"]),
                            "nanogram per liter": (0.000001, []),
                          }
}


## A few utilities
def Simplify(String):
    """
    Simplify(String)

    returns the string with the whitespace and capitalization removed
    """
    return "".join(String.lower().split())

def GetUnitTypes():
    """
    returns a list of all the unit types available

    a unit type is something like "mass", "velocity", etc.
    """
    return ConvertDataUnits.keys()

def GetUnitNames(UnitType):
    """
    returns a list of all the units available for a given unit type available

    a unit type is something like "mass", "velocity", etc.

    a unit of mass would be "kilogram", "slug", etc.
    """
    return ConvertDataUnits[UnitType].keys()

def FindUnitTypes():
    """
    returns a mapping of all the unit names to the unit types
    
    raises an exception if there is more than one option -- this will check
    the unit database for duplicated names

    Usually not called from user code.
    """
    unit_types = {}
    for unit_type in ConvertDataUnits.keys():
        if unit_type == "Oil Concentration" or unit_type == "Concentration In Water":
            continue # skipping Oil Concentration, 'cause this is really length -- lots of duplicate units!
                     # skipping Concentration in water, cause this has lots of duplicate units 
        for PrimaryName, data in ConvertDataUnits[unit_type].items():
            # strip out whitespace and capitalization
            #Pname = Simplify(PrimaryName)
            Pname = PrimaryName
            # add the primary name:
            unit_types[Pname] = unit_type
            # now the synonyms:
            for n in data[1]:
                if unit_type == "Volume" and n == 'oz':
                    continue # skip, "oz" is only mass
                if unit_types.has_key(n):
                    raise ValueError("Duplicate name in units table: %s"%n)
                unit_types[n] = unit_type
    return unit_types

def GetUnitAbbreviation(unit_type, unit):
    """
    return the standard abbreviation for a given unit
    
    :param unit_type: the type of unit: "mass", "length", etc.
    :param unit: the unit you want the abbreviation for: "gram", etc.
    """
    return ConvertDataUnits[unit_type][unit][1][0]

def is_same_unit(unit1, unit2):
    """
    Checks if the two unit names passed in are the same

    :param unit1: name of unit to compare
    :type unit1: string

    :param unit2: name of unit to compare
    :type unit2: string

    :returns: True if they are synonyms for the same unit.
              False if they are different units.
              False if one of them is not in the database.

    """
    all_types = FindUnitTypes()
    try:
        type1 = all_types[unit1]
        type2 = all_types[unit2]
    except KeyError:
        return False
    if type1 != type2:
        return False
    else:
        Synonyms = Converters[Simplify(type1)].Synonyms
        return Synonyms[Simplify(unit1)] == Synonyms[Simplify(unit2)]

class ConverterClass:
    """
    Main class for performing the conversion there will be one instance for each unit type

    sub-classes will handle special cases
    """
        
    def __init__(self, TypeName, UnitsDict):
        """
        Create a Converter

        :param TypeName: the name of the unit type, such as "length"
        :param UnitsDict: a dict will the unit data. See unit_data.py for format
        """
        self.Name = TypeName

        self.Synonyms = {}
        self.Convertdata = {}
        for PrimaryName, data in UnitsDict.items():
            # strip out whitespace and capitalization
            Pname = Simplify(PrimaryName)
            self.Convertdata[Pname] = data[0]
            self.Synonyms[Pname] = Pname
            for synonym in data[1]:
                self.Synonyms[Simplify(synonym)] = Pname

    def Convert(self, FromUnit, ToUnit, Value):

        """
        Convert(FromUnit, ToUnit, Value)

        returns a new value, in the units of ToUnit.

        :param FromUnit: the unit the original value is in
        :param ToUnit: the unit you want the value converted to
        :param Value: the original value
        """
        FromUnit = Simplify(FromUnit)
        ToUnit = Simplify(ToUnit)

        try:
            FromUnit = self.Synonyms[FromUnit]
        except KeyError:
            raise ValueError( "invalid unit: %s, %s"%(FromUnit, self.Name) )
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise ValueError( "invalid unit: %s, %s"%(ToUnit, self.Name) )

        return Value * self.Convertdata[FromUnit] / self.Convertdata[ToUnit]

# the special case classes:
class TempConverterClass(ConverterClass):
    """
    Special case class for temperature conversion.

    handles the zero-offset shift for K, C, F...
    """
    def Convert(self, FromUnit, ToUnit, Value):

        """
        Convert(FromUnit, ToUnit, Value)

        returns a new value, in the units of ToUnit.

        :param FromUnit: the unit the original value is in
        :param ToUnit: the unit you want the value converted to
        :param Value: the original value
        """

        FromUnit = Simplify(FromUnit)
        ToUnit = Simplify(ToUnit)

        try:
            FromUnit = self.Synonyms[FromUnit]
        except KeyError:
            raise ValueError( "invalid unit: %s, %s"%(FromUnit, self.Name) )
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise ValueError( "invalid unit: %s, %s"%(ToUnit, self.Name) )

        A1 = self.Convertdata[FromUnit][0]
        B1 = self.Convertdata[FromUnit][1]
        A2 = self.Convertdata[ToUnit][0]
        B2 = self.Convertdata[ToUnit][1]

        to_val = ((Value + B1)*A1/A2)-B2

        return to_val

class DensityConverterClass(ConverterClass):
    """
    Special case class for Density conversion.

    handles the special case of API gravity, etc.
    """

    def Convert(self, FromUnit, ToUnit, Value):

        """
        Convert(FromUnit, ToUnit, Value)

        returns a new value, in the units of ToUnit.

        :param FromUnit: the unit the original value is in
        :param ToUnit: the unit you want the value converted to
        :param Value: the original value
        """

        FromUnit = Simplify(FromUnit)
        ToUnit = Simplify(ToUnit)
         
        try:
            FromUnit = self.Synonyms[FromUnit]
        except KeyError:
            raise ValueError( "invalid unit: %s, %s"%(FromUnit, self.Name) )
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise ValueError( "invalid unit: %s, %s"%(ToUnit, self.Name) )
        if FromUnit == "apidegree": # another Special case (could I do this the same as temp?)
            Value = 141.5/(Value + 131.5)
            FromUnit = u"specificgravity(15\xb0c)"
        if ToUnit == "apidegree":
            ToVal = 141.5/(Value * self.Convertdata[FromUnit] / self.Convertdata[u"specificgravity(15\xb0c)"] ) - 131.5
        else:
            ToVal = Value * self.Convertdata[FromUnit] / self.Convertdata[ToUnit]
        return ToVal

class OilQuantityConverter:
    """
    class for Oil Quantity conversion -- mass to/from Volume

    requires density info as well
    """
    @classmethod
    def ToVolume(self, Mass, MassUnits, Density, DensityUnits, VolumeUnits):
        """
        Convert Oil Mass to Volume

        :param Mass: mass you want converted to volume
        :param MassUnits: unit of mass input
        :param Density: density of oil 
        :param DensityUnits: units of density
        :param VolumeUnits: units of volume desired

        """
        Density = convert("Density", DensityUnits, "kg/m^3", Density)
        #print "Density in kg/m^3", Density
        Mass = convert("Mass", MassUnits, "kg", Mass)
        #print "Mass in kg", Mass
        Volume = Mass / Density
        #print "Volume in m^3", Volume
        Volume = convert("Volume", "m^3", VolumeUnits, Volume)
        #print "Volume in %s"%VolumeUnits, Volume
        return Volume
    @classmethod
    def ToMass(self, Volume, VolUnits, Density, DensityUnits, MassUnits):
        """
        Convert Oil Mass to Volume

        :param Volume: volume you want converted to mass
        :param VolumeUnits: units of volume input
        :param Density: density of oil 
        :param DensityUnits: units of density
        :param MassUnits: unit of mass desired for output
        """

        Density = convert("Density", DensityUnits, "kg/m^3", Density)
        #print "Density in kg/m^3", Density
        Volume = convert("Volume", VolUnits, "m^3", Volume)
        #print "Volume in m^3", Volume
        Mass = Volume * Density
        #print "Mass in kg", Mass
        Mass = convert("Mass", "kg", MassUnits,  Mass)
        #print "Mass in %s"%MassUnits, Mass
        return Mass

# create the converter objects
Converters = {}
for (unittype,data) in ConvertDataUnits.items():
    if unittype.lower() == 'temperature':
        Converters["temperature"] = TempConverterClass(unittype, data)
    elif unittype.lower() == 'density':
        Converters["density"] = DensityConverterClass(unittype, data)
    else:
        Converters[Simplify(unittype)] = ConverterClass(unittype, data)

def convert(UnitType, FromUnit, ToUnit, Value):
    """
    Convert(FromUnit, ToUnit, Value)

    returns a new value, in the units of ToUnit.

    :param FromUnit: the unit the original value is in
    :param ToUnit: the unit you want the value converted to
    :param Value: the original value
    """
    UnitType= Simplify(UnitType)
    try:
        Converter = Converters[UnitType]
    except:
        raise ValueError("Invalid unit type: %s"%UnitType)
    return Converter.Convert(FromUnit, ToUnit, Value )
    
Convert = convert # so to have the old, non-PEP8 compatible name

