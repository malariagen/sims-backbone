import { Component, OnInit, ViewChild, NgZone } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SearchApi, SearchRequest, AlfrescoApi, NodesApi } from '@alfresco/js-api';
import { AlfApiService } from '../alf-api.service';
import { FormGroup, FormBuilder } from '@angular/forms';

import { CdkTextareaAutosize } from '@angular/cdk/text-field';

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

  const description = _('sims.study.properties.description');
  const status = _('sims.study.properties.status');
  @ViewChild('autosize', { static: false }) autosize: CdkTextareaAutosize;

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
          "query": "select * from cmis:folder WHERE cm:name=" + this.studyCode,
          "language": "cmis"
        }
      };

      console.log(request);
      search.search(request).then((data) => {
        console.log('Search API called successfully. Returned data: ');
        console.log(data);

        const nodeId = 'd3ea4a15-89fe-45f9-b876-12dbc206e985';

        let nodesApi = new NodesApi(alfApi);

        let opts = {
          'include': ['association']
        };

        nodesApi.getNode(nodeId, opts).then((data) => {
          console.log('Node API called successfully. Returned data: ');
          console.log(data);
          this.studyProperties = data.entry.properties;
          this.studyNode = data.entry;

          this.studyForm = this._fb.group(
            {
              description: [this.studyProperties['cm:description'], []],
              status: [this.studyProperties['cggh:collaborationStatus'], []],
            });
        }, function (error) {
          console.error(error);
        });

      }, function (error) {
        console.error(error);
      });
    }
    );
  }

}
