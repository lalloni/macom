var app = {};

// Fields Defaults de aplicacion
app.fields = {
	InterfaceGridFields : [ mcm.fields.FormatedDirection, mcm.fields.FullName, mcm.fields.Technology, mcm.fields.Goal, mcm.fields.Published ],
	DependencyGridFields: [ mcm.fields.FormatedDirection, mcm.fields.Interface, mcm.fields.Technology, mcm.fields.Goal ],
	ReverseDependencyGridFields: [ mcm.fields.FormatedDirection, mcm.fields.ReverseDependencyFullName, mcm.fields.Technology, mcm.fields.Goal ],
	DependencyDatasourceFields: [ mcm.fields.InterfaceFullName ]
};


app.views = {
	show: function (viewer, record, recordNum, field, fieldNum, value, rawValue) {
	  
	  var idtab = "id" + record.resource_uri.replaceAll("/","");
	  var tab = ContentTabSet.getTab(idtab);

	  // si no se encuentra generar uno nuevo con titulo = record.name
	  if (tab == null || typeof (tab) == 'undefined') {

		var name = record.name;
		if ( record.full_name ) name = record.full_name;
		  
	  	var functionTabCallback = "";
		switch ( record.kind ){
			case "system":
				functionTabCallback = "app.views.showSystem";
				break;
			case "module":
				functionTabCallback = "app.views.showModule";
				break;
			case "interface":
				functionTabCallback = "app.views.showInterface";
				break;
			case "architecturalpattern":
				functionTabCallback = "app.views.showActhitecturalPattern";
				break;
			case "moduletype":
				functionTabCallback = "app.views.showModuleType";
				break;
			case "dependency":
				functionTabCallback = "app.views.showDependency";
				name = mcm.format.DependencyFullName( record );
				break;
		}
		
		// Agrega un nuevo tab
		ContentTabSet.addTab({
			ID : idtab,
			title : new mcm.IconsFactory(record).getNodeIcon() + " " + name,
	      	record : record
	    });

	    // Busca el tab recien creado
	    tab = ContentTabSet.getTab(idtab);

	    // Se fija el record.kind
	    if (record.kind == 'rootsystem') {
	        tab.setPane(app.views.getRootSystem(record));
	    } else if (record.kind == 'rootpattern') { 
	    	tab.setPane(app.views.getRootArchitecturalPattern(record));
	    } else if (record.kind == 'rootmoduletype') { 
	    	tab.setPane(app.views.getRootModuleType(record));
	    } else {
	    	// DATASOURCE
	        isc.JSONDataSource.create({
	          dataURL : record.resource_uri
	        }).fetchData(
	            null, functionTabCallback + "(data, \"" + idtab + "\")" // Callback
	        );
	    }
	  }
	  ContentTabSet.selectTab(tab);
	},
			
	getRootSystem: function (record) {
	  var tabset = new Array();

	  for ( var i = 0; i < record.diagrams.length; i++) {
	    tabset.push({
	      title : record.diagrams[i].name,
	      pane : isc.Diagram.create({
	        src : record.diagrams[i].diagram_uri
	      })
	    })
	  }
	  
	  tabset.push({
	      title : "Etiquetas",
	      pane : isc.TagCloud.create({
	    	  resource_uri: record.tagcloud_uri,
	    	  opener: "app.views.show"
	      })
	  });

	  return isc.TabSet.create({
	    tabs : tabset
	  });
	},
	
	getRootArchitecturalPattern: function (record) {
		return isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
		          dataURL : record.resource_uri,
		          autoFetchData : true,
		          fields : [ mcm.fields.Name, mcm.fields.CasesCount, mcm.fields.Description ],
		          transformResponse: function (dsResponse, dsRequest, data){
		        	  // Transforma propiedades de los items del menu a un formato unico
		        	  dsResponse.data = mcm.util.map( function (d){
		        		  // Cuenta de la cantidad de casos existentes por patrón
		        		  d.cases_count = (d.cases.length > 0?d.cases.length:"");

		        		  // Acordar descripciones largas
		        		  if ( d.description && d.description.length > 130 ){
		        			d.description = d.description.substr(0,130) + " ...";  
		        		  }
		        		  
		        		  return d;
		    		  }, data );
		          }
	        })
		})
	},

	getRootModuleType: function (record) {
		return this.getRootArchitecturalPattern(record);
	},
	
	showSystem: function (data, id) {
	  var system = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Sistema",
	    data : system,
	    fields : [ mcm.fields.Description, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation, mcm.fields.Tags ],
	    additionalInfo : [ {
	      title : "M&oacute;dulos ",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : system.modules_uri,
	          autoFetchData : true,
	          fields : [ mcm.fields.FormatedExternal, mcm.fields.FullName, mcm.fields.Goal ]
	        })
	      })
	    }, {
	      title : "Interfaces",
	      pane : isc.DetailGrid.create({
	    	initialCriteria: { published: true },
	    	fields: app.fields.InterfaceGridFields,
	    	dataSource : isc.JSONDataSource.create({
	          dataURL : system.interfaces_uri,
	          autoFetchData : true,
	          cacheAllData: true // Se utiliza para que initialCriteria actue al inicio
	        })
	      })
	    }, {
	      title : "Dependencias",
	      pane : isc.DetailGrid.create({
	    	fields : app.fields.DependencyGridFields,
	    	dataSource : isc.JSONDataSource.create({
	          dataURL : system.dependencies_uri,
	          autoFetchData : true,
	          cacheAllData: true,
	          fields: app.fields.DependencyDatasourceFields
	        })
	      })
	    }, {
	      title : "Dependencias inversas",
	      pane : isc.DetailGrid.create({
	    	fields : app.fields.ReverseDependencyGridFields,
	    	dataSource : isc.JSONDataSource.create({
	          dataURL : system.reverse_dependencies_uri,
	          autoFetchData : true,
	          fields: app.fields.DependencyDatasourceFields
	        })
	      })
	    } ]
	  }));
	},
	
	showModule: function (data, id) {
	  var module = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "M&oacute;dulo",
	    data : module,
	    fields : [ mcm.fields.Goal, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation, mcm.fields.Tags ],
	    additionalInfo : [ {
	      title : "Interfaces",
	      pane : isc.DetailGrid.create({
	    	fields : app.fields.InterfaceGridFields,
	        dataSource : isc.JSONDataSource.create({
	          dataURL : module.interfaces_uri,
	          autoFetchData : true
	        })
	      })
	    }, {
	      title : "Dependencias",
	      pane : isc.DetailGrid.create({
	    	fields : app.fields.DependencyGridFields,
	    	dataSource : isc.JSONDataSource.create({
	          dataURL : module.dependencies_uri,
	          autoFetchData : true,
	          fields: app.fields.DependencyDatasourceFields
	        })
	      })
	    }, {
	      title : "Dependencias inversas",
	      pane : isc.DetailGrid.create({
	    	fields : app.fields.ReverseDependencyGridFields,
	    	dataSource : isc.JSONDataSource.create({
	          dataURL : module.reverse_dependencies_uri,
	          autoFetchData : true,
	          fields: app.fields.DependencyDatasourceFields
	        })
	      })
	    } ]
	  }));
	},
	
	showInterface: function (data, id) {
	  var interface = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Interface",
	    data : interface,
	    fields : [ mcm.fields.Goal, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation, mcm.fields.Technology, mcm.fields.Published, mcm.fields.Tags ],
	    additionalInfo : [ {
	        title : "Dependencias inversas",
	        pane : isc.DetailGrid.create({
	          fields : app.fields.ReverseDependencyGridFields,
	          dataSource : isc.JSONDataSource.create({
	            dataURL : interface.reverse_dependencies_uri,
	            autoFetchData : true,
		        fields: app.fields.DependencyDatasourceFields
	          })
	        })
	      } ]
	  }));
	},
	
	showDependency:	function (data, id) {
	  var dependency = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Dependencia a la interfaz",
	    formatTitleValue: mcm.format.DependencyFullName,
	    data : dependency,
	    fields : [ mcm.fields.Goal, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation, mcm.fields.Technology ],
	    additionalInfo : [ {
	      title : "Interfaz utilizada",
	      pane : isc.DetailGrid.create({
	    	  fields : app.fields.InterfaceGridFields,
	          dataSource : isc.JSONDataSource.create({
	            dataURL : dependency.interface.resource_uri,
	            autoFetchData : true
	          })
	      })
	    } ]
	  }));
	},
	
	showActhitecturalPattern: function (data, id) {
	  var pattern = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Patrón",
	    data : pattern,
	    fields : [ mcm.fields.Name, mcm.fields.Description, mcm.fields.Tags ],
	    additionalInfo : [{
	      title : "Casos",
	      pane : isc.DetailGrid.create({
	    	  fields : [ mcm.fields.FormatedExternal, mcm.fields.ModuleFullName, mcm.fields.Goal ],
	          data: mcm.util.map( function (c){ return c.module; }, pattern.cases)
	      })
	    }]
	  }));
	},

	showModuleType: function (data, id) {
	  var moduletype = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Típo de Módulo",
	    data : moduletype,
	    fields : [ mcm.fields.Name, mcm.fields.Description],
	    additionalInfo : [{
	      title : "Casos",
	      pane : isc.DetailGrid.create({
	    	  fields : [ mcm.fields.FormatedExternal, mcm.fields.ModuleFullName, mcm.fields.Goal ],
	          data: mcm.util.map( function (c){ return c.module; }, moduletype.cases)
	      })
	    }]
	  }));
	}
}


isc.DetailGrid.addProperties({
  recordDoubleClick : app.views.show
});

isc.ItemViewer.addProperties({
  opener: "app.views.show"	
})

//Layout principal
isc.VLayout.create({
  width : "100%",
  height : "100%",
  members : [ isc.HStack.create({
    ID : "HeaderSection",
    height : 48,
    hPolicy : "fill",
    members : [ isc.Label.create({
      contents : "macom",
      baseStyle : "header"
    }), isc.LayoutSpacer.create({
      width : "*"
    }), isc.Img.create({
      doubleClick: function() { isc.showConsole(); },
      imageType : "natural",
      src : "grass.png"
    }) ]
  }), isc.HLayout.create({
    ID : "ContentSection",
    height : "*",
    showEdges : "true",
    members : [ isc.TreeGrid.create({
      ID : "NavigationTree",
      width : 300,
      showResizeBar : true,
      generateClickOnEnter : true,
      showHeader: false,
      showOpenIcons:false,
      showDropIcons:false,	
      closedIconSuffix:"",
      dataProperties : {
        openProperty : "isOpen"
      },
      getIcon : function(node) {
    	  // todo: implementar IconsFactory
    	  return "/media/img/" + node.kind + (node.external ? "-external" : "") + ".png";
      },
      dataSource : isc.JSONDataSource.create ({
          dataURL : "",
          fields : [ {
        	  name : "name"
          } ],
          transformRequest: function (dsRequest){
        	  if ( dsRequest.parentNode.childs_uri ){
        		  this.dataURL = dsRequest.parentNode.childs_uri;
        	  } else {
        	  	this.dataURL = dsRequest.parentNode.resource_uri;
        	  }
          },
          transformResponse: function (dsResponse, dsRequest, data){
        	  // Transforma propiedades de los items del menu a un formato unico
        	  dsResponse.data = mcm.util.map( function (d){
    			  var isfolder = true;
    			  var childs_uri = "";
            	  
    			  switch ( d.kind ){
	       	  	 	case "rootsystem":
	       	  	 		childs_uri = d.resource_uri;
	       	  	 		break;
	       	  	 	case "system":
	       	  	 		childs_uri = d.modules_uri;
	       	  	 		break;
	       	  	 	case "module": childs_uri = d.interfaces_uri;
	       	  	 		break;
	       	  	 	case "architecturalpatterncase":
	       	  	 	case "architecturalpattern":
	       	  	 		d.full_name = d.name;
	       	  	 	case "interface":
	       	  	 	case "moduletype":
	       	  	 		isfolder = false;
	       	  	 		break;
	       	  	 	case "rootpatterns":
	          	  }

        		  return {Id:d.resource_uri,
				  	  resource_uri: d.resource_uri,
				  	  childs_uri : childs_uri,
				  	  name: d.name,
				  	  full_name: d.full_name,
				  	  kind: d.kind,
				  	  external: d.external,
				  	  isFolder: isfolder};
    		  }, data );
          }
      }),
      initialData: isc.Tree.create({
          nameProperty: "Name",
          idField: "Id",
          data: [{
          	Id:"system",
          	resource_uri: "{% url api_system_list %}",
          	name: "Sistemas",
          	full_name: "Sistemas",
          	kind: "rootsystem",
            tagcloud_uri : "{% url api_tag_list %}",
            diagrams: [{
            	name: "Dependencias entre sistemas",
                diagram_uri: "{% url web:systems_dependencies_diagram %}"
				},{
	            name: "Dependencias entre sistemas (excluyendo externos)",
	            diagram_uri: "{% url web:systems_no_thirdparty_dependencies_diagram %}"
	        }]
          },{
          	Id:"pattern",
          	resource_uri: "{% url api_architecturalpattern_list %}",
          	name:"Patrones",
          	full_name: "Patrones",
          	kind: "rootpattern"
          },{
            Id:"moduletype",
            resource_uri: "{% url api_moduletype_list %}",
            name:"Típos de Módulo",
            full_name: "Típos de Módulo",
            kind: "rootmoduletype"
          }]
      }),
      fields : [ {
        name : "name",
        recordDoubleClick : app.views.show
      } ],
      recordDoubleClick : function() {
        // Elimina el evento de dobleClick por default
      }
    }), isc.TabSet.create({
      ID : "ContentTabSet",
      canCloseTabs : true,
      closeTabIconSize : 12
    }) ]
  }) ]
});

// INIT

// Abre el primer item de NavigationTree 
app.views.show(null, NavigationTree.initialData.root.children[0]);
NavigationTree.getData().openAll();
