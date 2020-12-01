import React from "react";
import "./App.css";
import mondaySdk from "monday-sdk-js";
import Container from "react-bootstrap/Container";
import Row from  "react-bootstrap/Row";
import Col from  "react-bootstrap/Col";
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

const monday = mondaySdk();

class App extends React.Component {
	constructor(props) {
		super(props);

		// Default state
		this.state = {
			settings: {},
			allItemIds: [],
			componentMap: {},
			tableRender: [],
			modulesMap: {},
			loader: true
		};
	}

	componentDidMount() {
	// TODO: set up event listeners

		monday.listen("context", this.getContext);
	}

	getContext = (res) => {
		const context = res.data;
		console.log("context!", context);
		this.setState({ context });

		const boardIds = context.boardIds || [context.boardId];

		var allItemIds = [];
		var componentMap = {}
		let boardIdForTable;

		monday
		.api(`query { boards(ids:[${boardIds}]) { id, items { id, column_values { id, value } } }}`)
		.then((res) => {
			console.log(res)

			res.data.boards[0].items.forEach((item, item_index) => {

				console.log(item.id)

				allItemIds.push(item.id);
				componentMap[item.id] = []

				item.column_values.forEach((column_value, column_index) => {

					if(column_value.id != 'creation_log' && column_value.id != 'last_updated'){

						let linkedPulseIds = JSON.parse(column_value.value);
						console.log(linkedPulseIds, boardIdForTable)

						if(linkedPulseIds != undefined && linkedPulseIds.linkedPulseIds != undefined){

							linkedPulseIds.linkedPulseIds.forEach((linkedPulseId, i) => {

								componentMap[item.id].push(linkedPulseId.linkedPulseId);

								if(boardIdForTable == undefined) {

									boardIdForTable = linkedPulseId.linkedPulseId;
								}
							});
						}
					}
				});
			});

			monday
				.api(`query { items (ids:[${boardIdForTable}]) { id, name, board { id } }}`)
				.then((res) => {

					console.log(allItemIds, componentMap);
					this.setState({allItemIds: allItemIds, componentMap: componentMap});
					this.getData(res.data.items[0].board.id)
				}
			);

		});
	};

	getData(boardIds){

		monday
		  .api(`query { boards(ids:[${boardIds}]) { id, items { id, column_values { id, value } } }}`)
		  .then((res) => {
			  console.log(res)

			  var tablesData = [];
			  var allItemIds = [];
			  res.data.boards[0].items.forEach((item, item_index) => {

				  console.log(item.id)

				  allItemIds.push(item.id);

				  var tableColumnItemIds = [];
				  item.column_values.forEach((column_value, column_index) => {

					  if(column_value.id == 'subitems' && column_value.value != null){

						  let linkedPulseIds = JSON.parse(column_value.value);

						  console.log(linkedPulseIds);

						  linkedPulseIds.linkedPulseIds.forEach((linkedPulseIdsItem, linkedPulseIdsIndex) => {

							  tableColumnItemIds.push(String(linkedPulseIdsItem.linkedPulseId))
							  allItemIds.push(String(linkedPulseIdsItem.linkedPulseId));
						  });
					  }
				  })

				  tablesData.push({

					  tableItemId: item.id,
					  tableColumnItemIds: tableColumnItemIds
				  });
			  });

			  this.getTableData(tablesData, allItemIds);
		  });
	}

	getTableData(tablesData, allItemIds, componentMap){

	  console.log(tablesData, allItemIds);

	  var tableRender = []
	  monday
		.api(`query { items (ids:[${allItemIds}]) { id, name, column_values { id, text } }}`)
		.then((res) => {

			console.log(res);

			var responseMap = {};

			res.data.items.forEach((item, itemIndex) => {

				responseMap[item.id] = itemIndex;
			});

			var tablesMap = {}

			tablesData.forEach((tableData, tableIndex) => {

				console.log(res.data.items[responseMap[tableData.tableItemId]].name)

				tablesMap[res.data.items[responseMap[tableData.tableItemId]].name] = tableIndex;
				tableRender.push({

					itemId: tableData.tableItemId,
					name: res.data.items[responseMap[tableData.tableItemId]].name
				});
			});

			console.log(responseMap, tablesMap)

			tablesData.forEach((tableData, tableIndex) => {

				var columns = [];

				tableData.tableColumnItemIds.forEach((tableColumnItemId, tableColumnItemIdIndex) => {

					var columnType = undefined;
					var forgienKey = undefined;

					res.data.items[responseMap[tableColumnItemId]].column_values.forEach((column_value, column_index) => {

						if(column_value.id == 'dropdown'){

							columnType = column_value.text;
						}

						if(column_value.id != 'dropdown' && column_value.id != 'creation_log' && column_value.id != 'last_updated'){

							forgienKey = column_value.text;
						}
					})

					if(columnType == 'Foreign'){

						columns.push({

							name: res.data.items[responseMap[tableColumnItemId]].name,
							type: columnType,
							forgienKeyTable: tablesMap[forgienKey]
						})
					}
					else{

						columns.push({

							name: res.data.items[responseMap[tableColumnItemId]].name,
							type: columnType
						})
					}
				});

				tableRender[tableIndex].columns = columns;
			});

			console.log(tableRender)
			this.setState({ tableRender: tableRender })

			this.getComponentData(allItemIds, componentMap)

		});
	}

	getComponentData(allItemIds, componentMap){

		console.log(this.state.allItemIds, this.state.componentMap);

		monday
		.api(`query { items (ids:[${this.state.allItemIds}]) { id, name, column_values { id, text }, group { id, title } }}`)
		.then((res) => {

			console.log(res);

			let modulesMap = {}

			res.data.items.forEach(item => {
				if(modulesMap[item.group.title] == undefined){

					modulesMap[item.group.title] = [];
				}

				let tables = '';

				item.column_values.forEach((column_value, column_index) => {

					if(column_value.id != 'creation_log' && column_value.id != 'last_updated'){

						tables = column_value.text;
					}
				});

				item.tables = tables;

				modulesMap[item.group.title].push(item);
			});

			console.log(modulesMap)
			this.setState({modulesMap: modulesMap});
			this.setState({loader: false})
		});
	}

	build(){

		this.setState({loader: true})

		console.log(this.state.modulesMap, this.state.tableRender)

		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ modulesMap: this.state.modulesMap, tableRender: this.state.tableRender })
		};
		fetch('https://nobrainer.in/common/service', requestOptions)
			.then(response => response.json())
			.then(data => {

				console.log(data);
				this.setState({loader: false})

				window.open('https://nobrainer.in/static/' + data.build);
			});
	}

  render() {
		return (
			<div className="App">
				<Container fluid>
					{
						(this.state.loader) ?
						<Row>
							<Col sm={12} className="text-center">
								<Spinner animation="grow" />
							</Col>
						</Row>
						:
						<Row>
							{Object.keys(this.state.modulesMap).map((module, index) => (
								<Col sm={6} key={index}>
									<Row>
										<Col sm={12}>
											<Table striped bordered hover variant="dark">
												<thead>
													<tr className="text-center">
														<th style={{color: '#dc3545'}}>{module}</th>
													</tr>
												</thead>
												<tbody>
													{this.state.modulesMap[module].map((component, index) => (
														<tr key={index}>
															<td>
																<Container >
																	<Row>
																		<Col sm={4} style={{color: '#007bff', paddingTop: 10, paddingBottom: 10}}>
																			<b>{component.name}</b>
																		</Col>
																		<Col sm={8} style={{color: '#ffc107', paddingTop: 10, paddingBottom: 10}}>
																			<b>{component.tables}</b>
																		</Col>
																	</Row>
																</Container>
															</td>
														</tr>
													))}
												</tbody>
											</Table>
										</Col>
									</Row>
								</Col>
							))}
							<Col sm={12} style={{textAlign:'right', paddingTop: 10, paddingBottom: 10}}>
								<Button variant="success" onClick={e => this.build()}>Build</Button>
							</Col>
						</Row>
					}
				</Container>
			</div>
		);
	}
}

export default App;
