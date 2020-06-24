using System.Collections;
using System.Collections.Generic;
using UnityEngine;
#pragma warning disable 1591
namespace DG.Tweening
{
    public class DOTweenTrigger : MonoBehaviour
    {
        public bool triggerOnEnable;
        public bool getCompsAlways = false;

        private DOTweenAnimation[] mAnimas;

        private void Awake()
        {
            if (!getCompsAlways)
                mAnimas = GetComponentsInChildren<DOTweenAnimation>(true);
        }

        public void OnEnable()
        {
            if (triggerOnEnable)
                DoTrigger();
        }

        public void DoTrigger()
        {
            if (getCompsAlways)
                mAnimas = GetComponentsInChildren<DOTweenAnimation>(true);
            foreach (var ani in mAnimas)
            {
                ani.DORestart();
            }
        }
    }
}