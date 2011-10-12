from pyparsing import *

# define number as a set of words
units = oneOf("Zero One Two Three Four Five Six Seven Eight Nine Ten"
          "Eleven Twelve Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen",
          caseless=True)
tens = oneOf("Ten Twenty Thirty Forty Fourty Fifty Sixty Seventy Eighty Ninety",caseless=True)
hundred = CaselessLiteral("Hundred")
thousand = CaselessLiteral("Thousand")
OPT_DASH = Optional("-")
numberword = ((( units + OPT_DASH + Optional(thousand) + OPT_DASH + 
                  Optional(units + OPT_DASH + hundred) + OPT_DASH + 
                  Optional(tens)) ^ tens ) 
               + OPT_DASH + Optional(units) )

# number can be any of the forms 123, 21B, 222-A or 23 1/2
housenumber = originalTextFor( numberword | Combine(Word(nums) + 
                    Optional(OPT_DASH + oneOf(list(alphas))+FollowedBy(White()))) + 
                    Optional(OPT_DASH + "1/2")
                    )
numberSuffix = oneOf("st th nd rd").setName("numberSuffix")
streetnumber = originalTextFor( Word(nums) + 
                 Optional(OPT_DASH + "1/2") +
                 Optional(numberSuffix) )

# just a basic word of alpha characters, Maple, Main, etc.
name = ~numberSuffix + Word(alphas)

# types of streets - extend as desired
type_ = Combine( MatchFirst(map(Keyword,"Street St Boulevard Blvd Lane Ln Road Rd Avenue Ave "
                        "Circle Cir Cove Cv Drive Dr Parkway Pkwy Court Ct Square Sq"
                        "Loop Lp".split())) + Optional(".").suppress())

# street name 
nsew = Combine(oneOf("N S E W North South East West NW NE SW SE") + Optional("."))
streetName = (Combine( Optional(nsew) + streetnumber + 
                        Optional("1/2") + 
                        Optional(numberSuffix), joinString=" ", adjacent=False )
                ^ Combine(~numberSuffix + OneOrMore(~type_ + Combine(Word(alphas) + Optional("."))), joinString=" ", adjacent=False) 
                ^ Combine("Avenue" + Word(alphas), joinString=" ", adjacent=False)).setName("streetName")

# PO Box handling
acronym = lambda s : Regex(r"\.?\s*".join(s)+r"\.?")
poBoxRef = ((acronym("PO") | acronym("APO") | acronym("AFP")) + 
             Optional(CaselessLiteral("BOX"))) + Word(alphanums)("boxnumber")

# basic street address
streetReference = streetName.setResultsName("name") + Optional(type_).setResultsName("type")
direct = housenumber.setResultsName("number") + streetReference
intersection = ( streetReference.setResultsName("crossStreet") + 
                 ( '@' | Keyword("and",caseless=True)) +
                 streetReference.setResultsName("street") )
streetAddress = ( poBoxRef("street")
                  ^ direct.setResultsName("street")
                  ^ streetReference.setResultsName("street")
                  ^ intersection )

tests = """\
    3120 De la Cruz Boulevard
    100 South Street
    123 Main
    221B Baker Street
    10 Downing St
    1600 Pennsylvania Ave
    33 1/2 W 42nd St.
    454 N 38 1/2
    21A Deer Run Drive
    256K Memory Lane
    12-1/2 Lincoln
    23N W Loop South
    23 N W Loop South
    25 Main St
    2500 14th St
    12 Bennet Pkwy
    Pearl St
    Bennet Rd and Main St
    19th St
    1500 Deer Creek Lane
    186 Avenue A
    2081 N Webb Rd
    2081 N. Webb Rd
    1515 West 22nd Street
    2029 Stierlin Court
    P.O. Box 33170
    The Landmark @ One Market, Suite 200
    One Market, Suite 200
    One Market
    One Union Square
    One Union Square, Apt 22-C
    """.split("\n")

# how to add Apt, Suite, etc.
suiteRef = (
            oneOf("Suite Ste Apt Apartment Room Rm #", caseless=True) + 
            Optional(".") + 
            Word(alphanums+'-')("suitenumber"))
streetAddress = streetAddress + Optional(Suppress(',') + suiteRef("suite"))

for t in map(str.strip,tests):
    if t:
        #~ print "1234567890"*3
        print t
        addr = streetAddress.parseString(t, parseAll=True)
        #~ # use this version for testing
        #~ addr = streetAddress.parseString(t)
        print "Number:", addr.street.number
        print "Street:", addr.street.name
        print "Type:", addr.street.type

