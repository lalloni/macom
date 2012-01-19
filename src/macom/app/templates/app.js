var app = {};

// Fields Defaults de aplicacion
app.fields = {
	InterfaceGridFields : [ mcm.fields.FormatedDirection, mcm.fields.FullName, mcm.fields.Technology, mcm.fields.Goal, mcm.fields.Published ],
	DependencyGridFields: [ mcm.fields.FormatedDirection, mcm.fields.Interface, mcm.fields.Technology, mcm.fields.Goal ],
	DependencyDatasourceFields: [ mcm.fields.InterfaceFullName ]
};

app.views = {
	show: function (viewer, record, recordNum, field, fieldNum, value, rawValue) {
	  var tab = ContentTabSet.getTab(record.resource_uri);

	  // si no se encuentra generar uno nuevo con titulo = record.name
	  if (tab == null || typeof (tab) == 'undefined') {

		var name = record.name;
		if ( record.full_name ) name = record.full_name;
		  
	  	var functionTabCallback = "app.views.show";
		switch ( record.kind ){
			case "root": functionTabCallback += "Root"; break;
			case "system": functionTabCallback += "System"; break;
			case "module": functionTabCallback += "Module"; break;
			case "interface": functionTabCallback += "Interface"; break;
			case "dependency":
				functionTabCallback += "Dependency";
				name = mcm.format.DependencyFullName( record );
			break;
		}

		// Recorda a 40 caracteres maximo
		//if( name && name.length ) {
			// name = (name.length > 40 ? "... " + name.substring(name.length - 40) : name);
		//}
		
		// Agrega un nuevo tab
		ContentTabSet.addTab({
	      ID : record.resource_uri,
	      title : new mcm.IconsFactory(record).getNodeIcon() + " " + name,
	      record : record
	    });

	    // Busca el tab recien creado
	    tab = ContentTabSet.getTab(record.resource_uri);

	    // Se fija el record.kind
	    if (record.kind == 'root') {
	        tab.setPane(app.views.showRoot(record));
	    } else {
	    	// DATASOURCE
	        isc.JSONDataSource.create({
	          ID : record.resource_uri,
	          dataURL : record.resource_uri
	        }).fetchData(
	            null, functionTabCallback + "(data, \"" + record.resource_uri + "\")" // Callback
	        );
	    }
	  }
	  ContentTabSet.selectTab(tab);
	},
			
	showRoot: function (record) {
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
	    	fields : app.fields.DependencyGridFields,
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
	    	fields : app.fields.DependencyGridFields,
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
	          fields : app.fields.DependencyGridFields,
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
          dataURL : "{% url api_system_list %}",
          fields : [ {
        	  name : "name"
          } ],
          transformRequest: function (dsRequest){
        	  if ( dsRequest.parentNode.childs_uri ){
        		  this.dataURL = dsRequest.parentNode.childs_uri;
        	  }
          },
          transformResponse: function (dsResponse, dsRequest, data){
        	  dsResponse.data = mcm.util.map( function (d){
    			  var isfolder = true;
    			  var childs_uri = "";
            	  
    			  switch ( d.kind ){
	       	  	 	case "root": childs_uri = d.resource_uri; break;
	       	  	 	case "system": childs_uri = d.modules_uri; break;
	       	  	 	case "module": childs_uri = d.interfaces_uri; break;
	       	  	 	case "interface":
	       	  	 		isfolder = false;
	       	  	 		break;
	       	  	 	case "dependency":
	       	  	 		break;
	          	  }

        		  return {Id:d.resource_uri,
				  	  resource_uri: d.resource_uri,
				  	  childs_uri : childs_uri,
				  	  name: d.name,
				  	  full_name: d.full_name,
				  	  kind: d.kind,
				  	  isFolder: isfolder};
    		  }, data );
          }
      }),
      initialData: isc.Tree.create({
          nameProperty: "Name",
          idField: "Id",
          data: [{
          	Id:"sistema",
          	resource_uri:
          	"/api/systems",
          	name:"Sistemas",
          	full_name: "Sistemas",
          	kind: "root",
            tagcloud_uri : "{% url api_tag_list %}",
            diagrams: [{
            	name: "Dependencias entre sistemas",
                diagram_uri: "{% url web:systems_dependencies_diagram %}"
				},{
	            name: "Dependencias entre sistemas (excluyendo externos)",
	            diagram_uri: "{% url web:systems_no_thirdparty_dependencies_diagram %}"
	        }]
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

// INITIAL STRIPT

// Abre el primer item de NavigationTree 
app.views.show(null, NavigationTree.initialData.root.children[0]);
NavigationTree.getData().openAll();
