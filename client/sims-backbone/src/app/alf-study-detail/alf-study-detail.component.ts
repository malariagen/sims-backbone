import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
//import { SearchApi, SearchRequest, AlfrescoApi, NodesApi } from '@alfresco/js-api';
//import { AlfApiService } from 'app/alf-api.service';

@Component({
  selector: 'app-alf-study-detail',
  templateUrl: './alf-study-detail.component.html',
  styleUrls: ['./alf-study-detail.component.scss']
})
export class AlfStudyDetailComponent implements OnInit {
  studyCode: string;

  studyProperties: {};
  studyNode: any;

  constructor(private route: ActivatedRoute/*, private alfrescoService: AlfApiService*/) {

  }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.studyCode = pmap.get('studyCode');
    });
    /*
        console.log("1");
        let alfApi = this.alfrescoService.alfrescoApi().then((alfApi: AlfrescoApi) => {
          console.log("2");
          console.log(alfApi);
          let search = new SearchApi(alfApi);
          console.log("3");
    
          let request: SearchRequest = {
            "query":
            {
              "query": "select * from cmis:folder WHERE cm:name=" + this.studyCode,
              "language": "cmis"
            }
          };

                search.search(request).then((data) => {
                  console.log('API called successfully. Returned data: ' + data);
                }, function (error) {
                  console.error(error);
                });
                
    let nodesApi = new NodesApi(alfApi);

    let opts = {
      'include': ['association']
    };

    nodesApi.getNode(nodeId, opts).then((data) => {
      console.log('API called successfully. Returned data: ' + data);
      console.log(data);
      this.studyProperties = data.entry.properties;
      this.studyNode = data.entry;
      console.log();
    }, function (error) {
      console.error(error);
    });
  });
  */
  }

}
