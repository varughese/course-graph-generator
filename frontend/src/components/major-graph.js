import DagreGraph from 'dagre-d3-react'
import courses from '../data/courses.json'
import '../styles/courses.css'
import React, { Component } from "react";

class MajorGraph extends Component {
  render()  {
	const nodes = courses.nodes.map(node => {
		node.label = `<h1>${node.id}</h1>`;
		node.labelType = 'html';
		return node;
	}).filter(node => Number(node.id.substring(3)) < 1551);
	const links = courses.links.filter(({source, target}) => {
		return !Number(source.substring(3)) < 1551 && Number(target.substring(3)) < 1551;
	});

	return (
		<DagreGraph
			nodes={nodes}
			links={links}
			options={{
				rankdir: 'TB',
				align: 'UL',
				ranker: 'tight-tree',
				edgesep: 4,
				ranksep: 120
			}}
			width={window.innerWidth}
			height='500'
			animate={1000}
			shape='rect'
			fitBoundaries
			zoomable
			onNodeClick={e => console.log(e)}
			onRelationshipClick={e => console.log(e)}
		/>
	)
  }
    
}

export default MajorGraph;