// Formateadores de fields
mcm.format = {
	InterfaceFullName : function ( value ){
		return value.module.system.name + ":" + value.module.name + ":" + value.name;
	},

	DependencyFullName : function ( value ){
		return mcm.format.InterfaceFullName( value.interface );
	}
}

// Fields Predefinidos

mcm.fields = {

  FullName : {
    name : "full_name",
    title : "Nombre"
  },

  Description : {
    name : "description",
    title : "Descripci&oacute;n"
  },

  Goal : {
    name : "goal",
    title : "Objetivo"
  },

  FunctionalReferents : {
    name : "functional_referents",
    title : "Referentes funcionales"
  },
  
  ImplementationReferents : {
    name : "implementation_referents",
    title : "Referentes de implementaci&oacute;n"
  },
  
  Documentation : {
    name : "documentation",
    title : "Documentaci&oacute;n"
  },

  Technology : {
    name : "technology",
    title : "Tecnolog&iacute;a",
    width : "100"
  },

  Direction : {
    name : "direction",
    title : "Flujo de información"
  },

  FormatedDirection : {
	name : "direction",
	title : "Flujo de información",
	width: "130px",
	type: "text",
	formatCellValue : function  (value, record, rowNum, colNum, grid) {
		var icons = new mcm.IconsFactory(record);
		var iconsHTML = icons.get("direction-in") + icons.get("direction-out"); 
		if ( iconsHTML.length > 0 ) return iconsHTML;
		else return icons.standaricon.error; 
	}
  },
  
  Published : {
	name : "published",
	title : "Publicada",
	width: "90px",
	valueMap: { true: "Si", false: "No" }
  },
  
  External : {
	name : "external",
	title : " "
  },

  FormatedExternal : {
	name : "external",
	title : " ",
	autoFitWidth: true,
	type: "text",
	formatCellValue : function  (value, record, rowNum, colNum, grid) {
		var icons = new mcm.IconsFactory(record);
		return icons.get("external"); 
	}
  },

  Interface : {
	name : "interface",
	title : "Interface"
  },
  
  InterfaceFullName: {
	name: "interface",
	formatCellValue: mcm.format.InterfaceFullName
  }
}
