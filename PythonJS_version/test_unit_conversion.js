var requirejs = require('requirejs');

requirejs.config({
    //Pass the top-level main.js/index.js require
    //function to requirejs so that node modules
    //are loaded relative to the top-level JS file.
    nodeRequire: require
});

var fs = require('fs');

// file is included here:
eval(fs.readFileSync('pythonjs-minimal.js')+'');

requirejs(
	['./unit_conversion.js'],
	function (uc) {
    //foo and bar are loaded according to requirejs
    //config, but if not found, then node's require
    //is used to load the module.
    console.log( 'I got this far' );
    console.log( 'the synonyms for meter are:');
    console.log( uc.ConvertDataUnits['Length']['meter'][1] );
    console.log( 'all the unit types are:');
    console.log( uc.GetUnitTypes() );
    console.log( "all the unit names of type Area are:" );
    console.log( uc.GetUnitNames('Area') );
    console.log( "the simplified version of a string is:")
    console.log( uc.Simplify("UGly  string WITH odd capitalIZATION"))
    ft = uc.Convert('length', 'meter', 'feet', 1.0);
    //console.log('meters to ft:')
    //console.log(ft)
});

