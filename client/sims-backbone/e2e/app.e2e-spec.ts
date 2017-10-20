import { SimsBackbonePage } from './app.po';

describe('sims-backbone App', () => {
  let page: SimsBackbonePage;

  beforeEach(() => {
    page = new SimsBackbonePage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
