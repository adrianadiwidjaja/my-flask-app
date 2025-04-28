const pushToDataFlow = require('../firebase/pushData');
const db = require('../firebase/firebase');

jest.mock('../firebase/firebase', () => {
  return {
    ref: jest.fn(() => ({
      push: jest.fn((value) => Promise.resolve({ wrote: value }))
    }))
  };
});

describe('pushToDataFlow', () => {
  test('pushes the provided payload under data_flow path', async () => {
    const data = { a: 1 };
    const ref = await pushToDataFlow(data);
    expect(db.ref).toHaveBeenCalledWith('data_flow');
    expect(ref).toEqual({ wrote: data });
  });
});
