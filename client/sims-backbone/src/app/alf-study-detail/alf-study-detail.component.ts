import { Component, OnInit, NgZone } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SearchApi, SearchRequest, AlfrescoApi, NodesApi } from '@alfresco/js-api';
import { AlfApiService } from '../alf-api.service';
import { FormGroup, FormBuilder } from '@angular/forms';

import { AngularEditorConfig } from '@kolkov/angular-editor';

import { marker as _ } from '@biesbjerg/ngx-translate-extract-marker';

@Component({
  selector: 'app-alf-study-detail',
  templateUrl: './alf-study-detail.component.html',
  styleUrls: ['./alf-study-detail.component.scss']
})
export class AlfStudyDetailComponent implements OnInit {
  studyCode: string;

  studyProperties: {};
  studyNode: any;

  description = _('sims.study.properties.description');
  descriptionApproved = _('sims.study.properties.descriptionApproved');

  status = _('sims.study.properties.status');
  webTitle = _('sims.study.properties.webTitle');
  webTitleApproved = _('sims.study.properties.webTitleApproved');

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

    let alfApi = this.alfrescoService.alfrescoApi().then((alfApi: AlfrescoApi) => {

      let search = new SearchApi(alfApi);

      let request: SearchRequest = {
        "query":
        {
          "query": "select * from cggh:collaboration WHERE cmis:name = \'" + this.studyCode + "\'",
          "language": "cmis"
        }
      };

      // console.log(request);
      search.search(request).then((data) => {
        // console.log('Search API called successfully. Returned data: ');
        // console.log(data);

        if (data.list.entries.length > 0) {
          const nodeId = data.list.entries["0"].entry.id;

          let nodesApi = new NodesApi(alfApi);

          let opts = {
            'include': ['association']
          };

          nodesApi.getNode(nodeId, opts).then((data) => {
            // console.log('Node API called successfully. Returned data: ');
            // console.log(data);
            this.studyProperties = data.entry.properties;
            this.studyNode = data.entry;

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
