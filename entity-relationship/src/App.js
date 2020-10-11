import React from "react";
import "./App.css";
import mondaySdk from "monday-sdk-js";
const monday = mondaySdk();

class App extends React.Component {
  constructor(props) {
    super(props);

    // Default state
    this.state = {
      settings: {},
      name: "",
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
    monday
      .api(`query { boards(ids:[${boardIds}]) { id, items { id, column_values { id, text, value, title, type } } }}`)
      .then((res) => {
        this.setState({ boards: res.data.boards }, () => {
            console.log(res)

          // console.log(res.data.boards[0].items.slice(0, 10).map((item) => item.id));
          // this.generateWords();
        });
      });
  };

  render() {
    return <div className="App">Hello, monday Apps!</div>;
  }
}

export default App;
