import { Component, OnInit, NgZone } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SearchApi, SearchRequest, AlfrescoApi, NodesApi } from '@alfresco/js-api';
import { AlfApiService } from '../alf-api.service';
import { FormGroup, FormBuilder } from '@angular/forms';

import { AngularEditorConfig } from '@kolkov/angular-editor';


@Component({
  selector: 'app-alf-study-detail',
  templateUrl: './alf-study-detail.component.html',
  styleUrls: ['./alf-study-detail.component.scss']
})
export class AlfStudyDetailComponent implements OnInit {
  studyCode: string;

  studyProperties: {};
  studyNode: any;

  editorConfig: AngularEditorConfig = {
    editable: false,
    showToolbar: false,
  };

  public studyForm: FormGroup;

  constructor(private route: ActivatedRoute, private alfrescoService: AlfApiService, private _fb: FormBuilder, private _ngZone: NgZone) {

  }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.studyCode = pmap.get('studyCode');
    });

    this.alfrescoService.alfrescoApi().then((alfApi: AlfrescoApi) => {

      const search = new SearchApi(alfApi);

      const request: SearchRequest = {
        'query':
        {
          'query': 'select * from cggh:collaboration WHERE cmis:name = \'' + this.studyCode + '\'',
          'language': 'cmis'
        }
      };

      // console.log(request);
      search.search(request).then((data) => {
        // console.log('Search API called successfully. Returned data: ');
        // console.log(data);

        if (data.list.entries.length > 0) {
          const nodeId = data.list.entries[0].entry.id;

          const nodesApi = new NodesApi(alfApi);

          const opts = {
            'include': ['association']
          };

          nodesApi.getNode(nodeId, opts).then((node) => {
            // console.log('Node API called successfully. Returned data: ');
            // console.log(data);
            this.studyProperties = node.entry.properties;
            this.studyNode = node.entry;

            this.studyForm = this._fb.group(
              {
                description: [this.studyProperties['cm:description'], []],
                descriptionApproved: [this.studyProperties['cggh:descriptionApproved'], []],
                status: [this.studyProperties['cggh:collaborationStatus'], []],
                webTitle: [this.studyProperties['cggh:webTitle'], []],
                webTitleApproved: [this.studyProperties['cggh:webTitleApproved'], []],

              });
          }, function (error) {
            console.error(error);
          });
        }

      }, function (error) {
        console.error(error);
      });
    }
    );
  }

}
