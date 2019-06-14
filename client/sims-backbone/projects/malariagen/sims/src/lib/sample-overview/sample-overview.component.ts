import { Component, OnInit, Input, AfterContentInit, OnChanges, SimpleChanges } from '@angular/core';
import { AssayData, DerivativeSamples, OriginalSamples, SamplingEvents } from '../typescript-angular-client';

import * as d3 from 'd3';

@Component({
  selector: 'sims-sample-overview',
  templateUrl: './sample-overview.component.html',
  styleUrls: ['./sample-overview.component.css']
})
export class SampleOverviewComponent implements AfterContentInit, OnChanges {
  
  height = 320;
  width = 400;
  svg: d3.Selection<d3.BaseType, {}, HTMLElement, any>;
  @Input()
  assayData: AssayData;

  @Input()
  derivativeSamples: DerivativeSamples;

  @Input()
  originalSamples: OriginalSamples;

  @Input()
  samplingEvents: SamplingEvents;

  constructor() { }

  ngAfterContentInit() {

  }

  ngOnChanges(changes: SimpleChanges): void {

    if (changes.derivativeSamples && !this.assayData) {
      // console.log(changes);
      this.buildGraph();
    }


  }

  buildGraph() {

    const nodes_data = [];

    const links_data = [];

    if (this.originalSamples) {
      this.originalSamples.original_samples.forEach(element => {
        let label: string;
        element.attrs.forEach(attr => {
          if (attr.attr_type === 'oxford_id') {
            label = attr.attr_value;
          }

        });
        nodes_data.push({
          'name': element.original_sample_id,
          'type': 'original',
          'label': label
        });

      });
    } else {
      return;
    }

    if (this.derivativeSamples) {
      this.derivativeSamples.derivative_samples.forEach(element => {
        let label: string;
        element.attrs.forEach(attr => {
          if (attr.attr_type === 'derivative_sample_source') {
            label = attr.attr_value;
          }

        });
        nodes_data.push({
          'name': element.derivative_sample_id,
          'type': 'derivative',
          'label': label
        });
        links_data.push({
          'source': element.original_sample_id,
          'target': element.derivative_sample_id,
          'type': 'original'
        })
      });
    }

    if (this.assayData) {

      this.assayData.assay_data.forEach(element => {
        let label: string = element.assay_datum_id;
        element.attrs.forEach(attr => {
          if (attr.attr_type === 'assay_datum_id') {
            label = attr.attr_value;
          }

        });
        nodes_data.push({
          'name': element.assay_datum_id,
          'type': 'assay',
          'label': label
        });
        links_data.push({
          'source': element.derivative_sample_id,
          'target': element.assay_datum_id
        })
      })
    }

    const simulation = d3.forceSimulation()
      .nodes(nodes_data);

    simulation
      .force('charge_force', d3.forceManyBody())
      .force('center_force', d3.forceCenter(this.width / 2, this.height / 2));

    // A bit crude...
    if (this.svg) {
      d3.select('svg').remove();
    }
    this.svg = d3.select('#graph').append('svg')
      .attr('width', this.width)
      .attr('height', this.height)
      .attr('preserveAspectRatio', 'xMinYMin slice')
      .append('g');


    function nodeColour(d) {
      if (d.type === 'original') {
        return 'blue';
      } else if (d.type === 'derivative') {
        return 'green';
      } else {
        return 'red';
      }
    }
    const node = this.svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(nodes_data)
      .enter().append('g')
      .attr('class', 'node');

    node.append('circle')
      .attr('r', 10)
      .style('fill', nodeColour);

    node/*.append("a")
    .attr('href', function (d) {
      return d.name;
    })*/
    .append('text')
      .style('text-anchor', 'middle')
      .text(function (d) {
        return d.label;
      });

    function linkColour(d) {
      if (d.type === 'original') {
        return 'blue';
      } else {
        return 'red';
      }
    }

    const link_force = d3.forceLink(links_data)
      .id(function (d) { return d['name']; })
      .strength(0.1);

    simulation.force('links', link_force)

      .force('charge', d3.forceManyBody().strength(function (d, i) {
        const a = i === 0 ? -1000 : -500;
        return a;
    }).distanceMin(200).distanceMax(500));

    const link = this.svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(links_data)
      .enter().append('line')
      .attr('stroke-width', 2)
      .attr('stroke', linkColour);

    function tickActions() {
      // update circle positions to reflect node updates on each tick of the simulation
      node.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
      /*
      node
        .attr("cx", function (d) { return d.x; })
        .attr("cy", function (d) { return d.y; });
        */

      // update link positions
      // simply tells one end of the line to follow one node around
      // and the other end of the line to follow the other node around
      link
        .attr('x1', function (d) { return d.source.x; })
        .attr('y1', function (d) { return d.source.y; })
        .attr('x2', function (d) { return d.target.x; })
        .attr('y2', function (d) { return d.target.y; });
    }


    simulation.on('tick', tickActions);
  }

}
