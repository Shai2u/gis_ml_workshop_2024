
def zoom_to_slected():
    # Get the active layer
    layer = iface.activeLayer()

    # Check if there is an active layer
    if layer:
        # Get the selected features
        selected_features = layer.selectedFeatures()

        # Select the features programmatically
        layer.selectByIds([feature.id() for feature in selected_features])

        # Zoom to the selected features
        iface.mapCanvas().zoomToSelected(layer)

    else:
        print("No active layer selected.")
        
        
    

def get_list_values(field_name):

    # Get the active layer
    layer = iface.activeLayer()

    # Replace 'field_name' with the name of the field you are interested in

    # Check if there is an active layer
    if layer:
        # Get the selected features
        selected_features = layer.selectedFeatures()

        # Get values for the specified field from selected features
        field_values = [feature[field_name] for feature in selected_features]

        # Print the values
        print(f"Values for {field_name} in selected features: {field_values}")
        return field_values

    else:
        print("No active layer selected.")
        

def filter_selected_layer(field_name):
    # Get the active layer
    layer = iface.activeLayer()

    # Replace 'field_name' with the name of the field you are interested in

     
    # Check if the selected layer exists
    if layer:
        # Get the selected features from the selected layer
        selected_features = layer.selectedFeatures()

        # Check if there are selected features
        if selected_features:
            # Get the value of the selected field from the first selected feature
            selected_value = selected_features[0][field_name]

            # Set up the expression for filtering in the selected layer
            filter_expression = QgsExpression(f'"{field_name}" = \'{selected_value}\'')

            # Create a feature request based on the expression
            #filter_request = QgsExpression.createExpressionContext().request()

            # Apply the filter to the selected layer
            layer.setSubsetString(filter_expression.expression())

            # Refresh the map canvas for the selected layer
            iface.mapCanvas().refresh()

        else:
            print("No features selected in the selected layer, Reset filter")
            # Apply the filter to the selected layer
            layer.setSubsetString('')

            # Refresh the map canvas for the selected layer
            iface.mapCanvas().refresh()
    else:
        print("Selected layer not found.")
