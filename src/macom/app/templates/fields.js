// Formateadores de fields
mcm.format = {
	InterfaceFullName : function (value, record, rowNum, colNum, grid) {
		return value.module.system.name + ":" + value.module.name + ":" + value.name;
	},

	DependencyFullName : function (value, record, rowNum, colNum, grid) {
		return value.interface.module.system.name + ":" + value.interface.module.name + ":" + value.interface.name;
	},
	
	ReverseDependencyFullName : function  (value, record, rowNum, colNum, grid) {
		return record.module.system.name + ":" + record.module.name;
	}

};

// Fields Predefinidos
mcm.fields = {
  Name : {
    name : "name",
    title : "Nombre",
    autoFitWidth: true
  },

  FullName : {
    name : "full_name",
    title : "Nombre",
    autoFitWidth: true
  },

  Kind : {
	name : "kind",
	title : "Tipo",
	autoFitWidth: true,	
	valueMap: { system: "Sistema", module: "Módulo", interface: "Interface" }
  },
  
  KindIcon : {
		name : "kindicon",
		title : " ",
		autoFitWidth: true,
		type: "text",
		formatCellValue : function  (value, record, rowNum, colNum, grid) {
			var icons = new mcm.IconsFactory(record);
			return icons.get("kind"); 
		}
   },
  
  Description : {
    name : "description",
    title : "Descripci&oacute;n"
  },

  DescriptionAndGoal : {
	  title: "Descripción / Objetivo",
	  formatCellValue: function (value, record, rowNum, colNum, grid) {
		  var desc = "";
		  if ( record.description ) desc += record.description; 
		  if ( record.goal ) desc += (desc.length > 0? "<br>":"") + record.goal;
		  return desc;
	  }
  },
  
  Tags : {
	name : "tags",
	title : "Etiquetas",
	formatCellValue : function (value, record, rowNum, colNum, grid) {
		return mcm.util.map(function(t) { return mcm.util.sprintf('<a href="#" onclick=\'mcm.showTag("%s","%s","%s")\'>%s</a> ', t.name, t.resource_uri, "app.views.show", t.name) }, value);
	}
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
	valueMap: { "true": "Si", "false": "No" }
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
  },

  ModuleFullName : {
	name : "full_name",
	title : "Módulo",
	autoFitWidth: true
  },
  CasesCount : {
	name : "cases_count",
	title : "# de casos",
	width: "70px"
  },
  
  ReverseDependencyFullName: {
	name: "reverseDependency",
	title : "Referenciado por",
	formatCellValue: mcm.format.ReverseDependencyFullName
  }
  
};
