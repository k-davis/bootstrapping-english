export interface VisualizationOptions {
  showAsHierarchy: boolean
  dataSource: 'opt1' | 'opt2' | 'opt3'
}

export const DefaultVisualizationOptions: VisualizationOptions = {
  showAsHierarchy: true,
  dataSource: 'opt1',
}
