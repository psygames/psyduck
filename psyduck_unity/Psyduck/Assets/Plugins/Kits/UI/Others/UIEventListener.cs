using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.Events;

public class UIEventListener : MonoBehaviour,
    IPointerClickHandler,
    IPointerDownHandler,
    IPointerUpHandler,
    IBeginDragHandler,
    IDragHandler,
    IEndDragHandler,
    IDropHandler
{
    public class InputEvent : UnityEvent<Vector2> { }

    public InputEvent onClick = new InputEvent();
    public InputEvent onDown = new InputEvent();
    public InputEvent onUp = new InputEvent();
    public InputEvent onBeginDrag = new InputEvent();
    public InputEvent onDrag = new InputEvent();
    public InputEvent onEndDrag = new InputEvent();
    public InputEvent onDrop = new InputEvent();

    public void OnPointerClick(PointerEventData eventData)
    {
        onClick?.Invoke(eventData.position);
    }

    public void OnPointerDown(PointerEventData eventData)
    {
        onDown?.Invoke(eventData.position);
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        onUp?.Invoke(eventData.position);
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
        onBeginDrag?.Invoke(eventData.position);
    }

    public void OnDrag(PointerEventData eventData)
    {
        onDrag?.Invoke(eventData.delta);
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        onEndDrag?.Invoke(eventData.position);
    }

    public void OnDrop(PointerEventData eventData)
    {
        onDrop?.Invoke(eventData.position);
    }
}
